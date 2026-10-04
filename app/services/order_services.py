from sqlalchemy.orm import Session

from app.models.order import Order

from app.repositories.inventory_repository import get_inventories_by_product
from app.repositories.order_repository import add_order

from app.services.inventory_services import deduct_stock

def create_order(
    db:Session,
    product_id:int,
    quantity:int
):
    try:
        inventories = get_inventories_by_product(
            db=db,
            product_id= product_id
        )
        
        if not inventories:
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
                db=db,
                product_id=product_id,
                warehouse_id=inventory.warehouse_id,
                quantity=quantity_to_deduct
            )
            
            remaining_quantity -= quantity_to_deduct
           
            
        new_order = Order(
                    product_id = product_id,
                    quantity = quantity,
                    status = "CONFIRMED"
                )
                
        add_order(
                        db=db,
                        order=new_order
                        )
                    
        return new_order
    
    except Exception:
        db.rollback()
        raise