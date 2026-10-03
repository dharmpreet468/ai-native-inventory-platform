from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.inventory import Inventory

def get_inventory(
    db: Session,
    product_id : int,
    warehouse_id : int
):
    
    return db.query(Inventory).filter(
        Inventory.product_id == product_id,
        Inventory.warehouse_id == warehouse_id
    ).first()
    
def check_stock(
    db:Session,
    product_id:int,
    warehouse_id:int,
    required_quantity:int
)-> bool:
        
        inventory = get_inventory(db,product_id,warehouse_id)
        
        if inventory is None:
            raise HTTPException(
                status_code=404,
                detail="inventory not not found"
            )
        
        return inventory.quantity >= required_quantity
    
def deduct_stock(
    db:Session,
    product_id:int,
    warehouse_id:int,
    quantity:int
):
    inventory = get_inventory(db,product_id,warehouse_id)
    
    if inventory is None:
        raise HTTPException(
            status_code= 404,
            detail="Inventory not found"
        )
    
    if inventory.quantity < quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient inventory"
        )
    
    inventory.quantity -= quantity
    
    return inventory