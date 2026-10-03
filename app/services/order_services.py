from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.inventory import Inventory
from app.services.inventory_services import deduct_stock

def create_order(
    db:Session,
    product_id:int,
    quantity:int
):
    inventories = db.query(Inventory).filter(
        Inventory.product_id == product_id
    ).order_by(Inventory.id)
    
    if inventories is None:
        raise ValueError("No inventory found for this product")
    
    total_available = sum(
        inventory.quantity
        for inventory in inventories
    )

    if total_available < quantity:
        raise ValueError("Insufficient inventory")
    
    remaining_quantity = quantity
    
    for inventory in inventories:
        if remaining_quantity <= 0:
            break
        
        quantity_to_deduct = min(remaining_quantity,inventory.quantity)
        
        deduct_stock(
            db = db,
            product_id = product_id,
            warehouse_id = inventory.warehouse_id,
            quantity=quantity_to_deduct
        )
        
        remaining_quantity -= quantity_to_deduct
        
        new_order = Order(
            product_id = product_id,
            quantity = quantity,
            status = "CONFIRMED"
        )
        
        db.add(new_order)
        
        return new_order