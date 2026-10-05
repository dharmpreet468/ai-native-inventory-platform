from sqlalchemy.orm import Session

from app.core.exceptions import (
    InventoryNotFoundException,
    InsufficientInventory,
    OrderNotFoundException,
    CancelledOrderException,
    OrderAlreadyConfirmedException
)

from app.models.order import Order

from app.repositories.inventory_repository import (
    get_inventories_by_product,
    get_inventory_by_id,
    restore_inventory_quantity
    )
from app.repositories.order_repository import (
    get_all_orders,
    get_order_by_id,
    add_order,
    update_order,
    add_order_allocation,
    get_order_allocations
)

from app.services.inventory_services import deduct_stock

def get_all_orders_service(db:Session):
    return get_all_orders(db=db)

def get_order_by_id_service(
    db:Session,
    order_id:int
):
    order = get_order_by_id(
        db=db,
        order_id=order_id
    )

    if order is None:
        raise OrderNotFoundException(order_id)

    return order

def create_order_service(
    db:Session,
    product_id:int,
    quantity:int
):
    try:
        inventories = get_inventories_by_product(
            db=db,
            product_id= product_id,
            for_update=True
        )

        if not inventories:
            raise InventoryNotFoundException(product_id)

        total_available = sum(
            inventory.quantity
            for inventory in inventories
        )

        if total_available < quantity:
            raise InsufficientInventory(
                product_id=product_id,
                requested=quantity,
                available= total_available
            )

        new_order = Order(
            product_id = product_id,
            quantity = quantity,
            status = "CONFIRMED"
        )

        add_order(db=db,order=new_order)

        # Required so new order is avialable
        db.flush()

        remaining_quantity = quantity

        for inventory in inventories:
            if remaining_quantity <= 0:
                break

            quantity_to_deduct = min(remaining_quantity,inventory.quantity)

            deduct_stock(
                db=db,
                product_id=product_id,
                warehouse_id=inventory.warehouse_id,
                quantity=quantity_to_deduct
            )

            add_order_allocation(
                db=db,
                order_id=new_order.id,
                inventory_id=inventory.id,
                quantity=quantity_to_deduct
            )

            remaining_quantity -= quantity_to_deduct

        return new_order

    except Exception:
        db.rollback()
        raise

def update_order_service(
    db:Session,
    order_id:int,
    update:dict
):
    order = get_order_by_id(
        db=db,
        order_id=order_id
    )

    if order is None:
        raise OrderNotFoundException(order_id)

    # Already Confirmed Order should not be modified

    if order.status == "CONFIRMED":
        raise OrderAlreadyConfirmedException(order_id)

    # Cancelled Order should not be modified

    if order.status == "CANCELLED":
        raise CancelledOrderException(order_id)

    return update_order(
        order=order,
        update = update
    )

def cancel_order_service(
    db:Session,
    order_id:int
):
    try:
        order = get_order_by_id(
            db=db,
            order_id=order_id,

        )

        if order is None:
            raise OrderNotFoundException(order_id)

        if order.status == "CANCELLED":
            raise CancelledOrderException(order_id)

        if order.status != "CONFIRMED":
            raise CancelledOrderException(order_id)

        allocations = get_order_allocations(
            db=db,
            order_id=order_id
        )

        for allocation in allocations:
            inventory = get_inventory_by_id(
                db=db,
                inventory_id=allocation.inventory_id,
                for_update = True
            )

            if inventory is None:
                raise InventoryNotFoundException(allocation.inventory_id)

            restore_inventory_quantity(
                inventory=inventory,
                quantity = allocation.quantity
            )

        order.status = "CANCELLED"
        return order

    except Exception:
        db.rollback()
        raise
