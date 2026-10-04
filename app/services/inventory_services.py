from sqlalchemy.orm import Session

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
    return get_inventory_by_id(
        db=db,
        inventory_id=inventory_id
    )


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
            raise ValueError("Inventory not found")
        
        return inventory.quantity >= required_quantity
    
def deduct_stock(
    db:Session,
    product_id:int,
    warehouse_id:int,
    quantity:int
):
    inventory = get_inventory(db,product_id,warehouse_id)
    
    if inventory is None:
        raise ValueError("Inventory not found")
    
    if inventory.quantity < quantity:
        raise ValueError("Insufficient inventory")
    
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
        raise ValueError("product not found")
    
    
    warehouse = get_warehouse_by_id(
        db=db,
        warehouse_id=warehouse_id
    )
    
    if warehouse is None:
        raise ValueError("warehouse not found")
    
    existing_inventory = get_inventory(
        db=db,
        product_id=product_id,
        warehouse_id=warehouse_id
    )
    
    if existing_inventory:
        existing_inventory.quantity += quantity
        return existing_inventory

    new_inventory = Inventory(
        product_id=product_id,
        warehouse_id=warehouse_id,
        quantity=quantity,
    )

    return add_inventory(
        db=db,
        inventory=new_inventory,
    )
   