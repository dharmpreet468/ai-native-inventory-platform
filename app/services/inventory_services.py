from sqlalchemy.orm import Session

from app.core.exceptions import (
    InventoryNotFoundException,
    ProductNotFoundException,
    WarehouseNotFoundException,
    InsufficientInventory,
    InventoryAlreadyExistsException
    )
from app.models.inventory import Inventory
from app.repositories.inventory_repository import (
    add_inventory,
    get_inventory,
    get_inventories_by_product,
    get_all_inventories,
    get_inventory_by_id,
    get_product_by_id,
    get_warehouse_by_id,
    update_inventory_quantity,
    update_inventory,
    delete_inventory,
    inventory_exists_for_product_warehouse
)

def get_inventory_service(
    db:Session,
    product_id:int,
    warehouse_id:int
):
    return get_inventory(
        db=db,
        product_id=product_id,
        warehouse_id=warehouse_id
    )


def get_all_inventory_service(db:Session):
    return get_all_inventories(db=db)

def get_inventory_by_id_service(
    db:Session,
    inventory_id:int
):
    inventory =  get_inventory_by_id(
        db=db,
        inventory_id=inventory_id
    )

    if inventory is None:
        raise InventoryNotFoundException(inventory_id)

    return inventory


def check_stock(
    db:Session,
    product_id:int,
    warehouse_id:int,
    required_quantity:int
)-> bool:

        inventory = get_inventory(
            db = db,
            product_id=product_id,
            warehouse_id = warehouse_id
        )

        if inventory is None:
            raise InventoryNotFoundException(product_id)

        return inventory.quantity >= required_quantity

def deduct_stock(
    db:Session,
    product_id:int,
    warehouse_id:int,
    quantity:int
):
    inventory = get_inventory(db,product_id,warehouse_id)

    if inventory is None:
        raise InventoryNotFoundException(product_id)

    if inventory.quantity < quantity:
        raise InsufficientInventory(product_id,quantity,inventory.quantity)

    new_quantity = inventory.quantity - quantity

    return update_inventory_quantity(
        inventory=inventory,
        quantity=new_quantity
    )

def create_or_update_inventory_service(
    db:Session,
    product_id:int,
    warehouse_id:int,
    quantity:int
):
    product = get_product_by_id(
        db=db,
        product_id=product_id
    )

    if product is None:
        raise ProductNotFoundException(product_id)


    warehouse = get_warehouse_by_id(
        db=db,
        warehouse_id=warehouse_id
    )

    if warehouse is None:
        raise WarehouseNotFoundException(warehouse_id)

    existing_inventory = get_inventory(
        db=db,
        product_id=product_id,
        warehouse_id=warehouse_id
    )

    if existing_inventory:
        raise InventoryAlreadyExistsException(
            product_id=product_id,
            warehouse_id=warehouse_id
        )

    new_inventory = Inventory(
        product_id=product_id,
        warehouse_id=warehouse_id,
        quantity=quantity,
    )

    return add_inventory(
        db=db,
        inventory=new_inventory,
    )


def update_inventory_service(
    db:Session,
    inventory_id:int,
    update:dict
):
    inventory = get_inventory_by_id(
        db=db,
        inventory_id=inventory_id
    )

    if inventory is None:
        raise InventoryNotFoundException(inventory_id)


    # Validation of product if it is being changed
    if "product_id" in update:
        product = get_product_by_id(
            db=db,
            product_id = update["product_id"]
        )

        if product is None:
            raise ProductNotFoundException(update["product_id"])

    # Validation of warehouse if it is being changed
    if "warehouse_id" in update:
        warehouse = get_warehouse_by_id(
            db=db,
            warehouse_id = update["warehouse_id"]
        )

        if warehouse is None:
            raise WarehouseNotFoundException(update["warehouse_id"])

    # Determine final product/warehouse combination
    final_product_id = update.get(
        "product_id",
        inventory.product_id
    )

    final_warehouse_id = update.get(
        "warehouse_id",
        inventory.warehouse_id
    )

    # prevent duplicate product + warehouse combination
    if inventory_exists_for_product_warehouse(
        db=db,
        product_id=final_product_id,
        warehouse_id=final_warehouse_id,
        exclude_inventory_id=inventory_id
    ):
        raise InventoryAlreadyExistsException(
            final_product_id,
            final_warehouse_id
        )

    return update_inventory(
        inventory=inventory,
        update=update
    )

def delete_inventory_service(
    db:Session,
    inventory_id:int
):
    inventory = get_inventory_by_id(
        db=db,
        inventory_id=inventory_id
    )
    if inventory is None:
        raise InventoryNotFoundException(inventory_id)

    return delete_inventory(
        db=db,
        inventory=inventory
        )
