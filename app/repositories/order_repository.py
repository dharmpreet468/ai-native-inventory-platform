from sqlalchemy.orm import Session

from app.models.order import Order

def get_all_orders(db:Session):
    return db.query(Order).all()

def get_order_by_id(order_id:int, db:Session):
    return db.query(Order).filter(
        Order.id == order_id
    ).first()
    
    
def add_order(
    db:Session,
    order:Order
):
    db.add(order)
    return order
    