from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.product import Product
from app.models.warehouse import Warehouse

def get_inventory(
    db:Session,
    product_id:int,
    warehouse_id:int
    ):
    return db.query(Inventory).filter(
        Inventory.product_id == product_id,
        Inventory.warehouse_id == warehouse_id
        ).first()

def get_inventories_by_product(
    db:Session,
    product_id:int,
    for_update:bool = False
):
    query = db.query(Inventory).filter(
        Inventory.product_id == product_id,
    ).order_by(
        Inventory.id
    )

    if for_update:
        query = query.with_for_update()

    return query.all()

def get_all_inventories(db:Session):
    return db.query(Inventory).all()

def get_inventory_by_id(
    db:Session,
    inventory_id:int,
    for_update:bool = False
):
    query = db.query(Inventory).filter(
        Inventory.id==inventory_id
    )

    if for_update:
        query = query.with_for_update()

    return query.first()

def get_product_by_id(
    db:Session,
    product_id:int
):
    return db.query(Product).filter(
        Product.id == product_id
    ).first()

def get_warehouse_by_id(
    db:Session,
    warehouse_id:int
):
    return db.query(Warehouse).filter(
        Warehouse.id == warehouse_id
    ).first()

def update_inventory_quantity(
   inventory:Inventory,
   quantity:int
):
    inventory.quantity = quantity

    return inventory

def add_inventory(
    db:Session,
    inventory:Inventory
):
    db.add(inventory)
    return inventory

def update_inventory(
    inventory:Inventory,
    update:dict
):
    for field,value in update.items():
        setattr(inventory,field,value)
    return inventory

def delete_inventory(
    db:Session,
    inventory:Inventory
):
    db.delete(inventory)


def inventory_exists_for_product_warehouse(
    db:Session,
    product_id:int,
    warehouse_id: int,
    exclude_inventory_id: int | None=None
):
    query = db.query(Inventory).filter(
        Inventory.product_id == product_id,
        Inventory.warehouse_id == warehouse_id
    )

    if exclude_inventory_id is not None:
        query = query.filter(
            Inventory.id != exclude_inventory_id
        )

    return query.first() is not None

def restore_inventory_quantity(
    inventory: Inventory,
    quantity: int
):
    inventory.quantity += quantity
    return inventory
