from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.repositories.order_repository import get_all_orders,get_order_by_id

from app.services.order_services import create_order 

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.get("/", response_model=list[OrderResponse])
def get_orders(db:Session=Depends(get_db)):
    return get_all_orders(db=db)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id:int,
    db:Session=Depends(get_db)
):
    order = get_order_by_id(
        db=db,
        order_id=order_id
    )
    
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
        return create_order(
           db=db,
           product_id = order.product_id,
           quantity = order.quantity
       )
   
   except ValueError as e:
       db.rollback()
       
       raise HTTPException(
           status_code = 400,
           detail=str(e)
       )
       
   except Exception:
       db.rollback()
       raise HTTPException(
           status_code=500,
           detail="Failed to create order"
       )
    