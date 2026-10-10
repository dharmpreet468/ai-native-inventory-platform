from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate

from app.services.order_services import (
    get_all_orders_service,
    get_order_by_id_service,
    create_order_service,
    update_order_service,
    cancel_order_service,
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.get("/", response_model=list[OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "manager", "employee")),
):
    return get_all_orders_service(db=db)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "manager", "employee")),
):
    return get_order_by_id_service(db=db, order_id=order_id)


@router.post("/", response_model=OrderResponse)
def create_order_endpoint(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "manager", "employee")),
):
    new_order = create_order_service(
        db=db,
        product_id=order.product_id,
        quantity=order.quantity,
    )

    db.commit()
    db.refresh(new_order)

    return new_order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order_put(
    order_id: int,
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "manager")),
):
    updates = order.model_dump()

    updated_order = update_order_service(db=db, order_id=order_id, update=updates)

    db.commit()
    db.refresh(updated_order)

    return updated_order


@router.patch("/{order_id}", response_model=OrderResponse)
def update_order_patch(
    order_id: int,
    order: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "manager")),
):
    updates = order.model_dump(exclude_unset=True)

    updated_order = update_order_service(db=db, order_id=order_id, update=updates)

    db.commit()
    db.refresh(updated_order)

    return updated_order


@router.delete("/{order_id}", response_model=OrderResponse)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    cancelled_order = cancel_order_service(db=db, order_id=order_id)

    db.commit()
    db.refresh(cancelled_order)

    return cancelled_order
