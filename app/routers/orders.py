from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_services import create_order 

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.get("/", response_model=list[OrderResponse])
def get_orders(db:Session=Depends(get_db)):
    return db.query(Order).all()

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id:int,
    db:Session=Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()
    
    if order is None:
        raise HTTPException(
            status_code = 404,
            detail="Order not found"
        )
    
    return order

@router.post("/",response_model=OrderResponse)
def create_order_endpoint(
    order: OrderCreate,
    db:Session=Depends(get_db)
):
   try:
       new_order = create_order(
           db=db,
           product_id = order.product_id,
           quantity = order.quantity
       )
       
       db.commit()
       db.refresh(new_order)
       
       return new_order
   
   except ValueError as e:
       db.rollback()
       raise HTTPException(
           status_code = 400,
           detail=str(e)
       )
       
   except Exception:
       raise HTTPException(
           status_code=500,
           detail="Failed to create order"
       )
    