from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles

from app.models.user import User

from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate
)

from app.services.product_services import(
    get_all_products_service,
    get_proudcts_by_id_service,
    create_product_service,
    update_product_service,
    delete_product_service
)



router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/",response_model=list[ProductResponse])
def get_products(
    db:Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin","manager","employee"))
    ):
    return get_all_products_service(db=db)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id:int,
    db:Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin","manager","employee"))
):

    return get_proudcts_by_id_service(
        db=db,
        product_id=product_id
    )

@router.post("/",response_model=ProductResponse)
def create_products(
    product:ProductCreate,
    db:Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
    ):
        new_product = create_product_service(
            db=db,
            name=product.name,
            price=product.price,
            category=product.category
        )

        db.commit()
        db.refresh(new_product)

        return new_product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product_put(
    product_id:int,
    product:ProductCreate,
    db:Session=Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    updates = product.model_dump()

    updated_product = update_product_service(
        db=db,
        product_id=product_id,
        update=updates
    )

    db.commit()
    db.refresh(updated_product)

    return updated_product

@router.patch("/{product_id}", response_model=ProductResponse)
def update_product_patch(
    product_id:int,
    product:ProductUpdate,
    db:Session=Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    updates = product.model_dump(exclude_unset=True)

    updated_product = update_product_service(
        db=db,
        product_id=product_id,
        update=updates
    )

    db.commit()
    db.refresh(updated_product)

    return updated_product

@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db:Session=Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    product = get_proudcts_by_id_service(
        db=db,
        product_id=product_id
    )
    delete_product_service(
        db=db,
        product=product
    )
    db.commit()
