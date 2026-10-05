from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_allocation import OrderAllocation

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

def update_order(
    order:Order,
    update:dict
):

    for field,value in update.items():
       setattr(order,field,value)

    return order

def add_order_allocation(
    db:Session,
    order_id:int,
    inventory_id:int,
    quantity:int
):
    allocation = OrderAllocation(
        order_id=order_id,
        inventory_id=inventory_id,
        quantity=quantity
    )

    db.add(allocation)
    return allocation

def get_order_allocations(
    db:Session,
    order_id:int
):
    return db.query(OrderAllocation).filter(
        OrderAllocation.order_id == order_id
    ).all()
