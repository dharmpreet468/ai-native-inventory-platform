from sqlalchemy.orm import Session

from app.core.exceptions import (
    ProductNotFoundException,
    ProductHasInventoryException,
    ProductHasOrderException
)
from app.models.product import Product
from app.repositories.product_repository import (
    get_all_products,
    get_products_by_id,
    update_product,
    delete_product,
    add_product,
    has_inventory,
    has_order
)

def get_all_products_service(db:Session):
    return get_all_products(db=db)

def get_proudcts_by_id_service(
    db:Session,
    product_id:int
):
    product = get_products_by_id(
        db=db,
        product_id=product_id
    )

    if product is None:
        raise ProductNotFoundException(product_id)

    return product

def create_product_service(
    db:Session,
    name:str,
    price:float,
    category:str
):
    product = Product(
        name = name,
        price = price,
        category = category
    )

    return add_product(
        db=db,
        product=product
    )


def update_product_service(
    db:Session,
    product_id:int,
    update:dict
):
    product = get_products_by_id(
        db=db,
        product_id=product_id
    )

    if product is None:
        raise ProductNotFoundException(product_id)

    return update_product(
        product=product,
        update=update
    )

def delete_product_service(
        db:Session,
        product:Product
    ):

        if product is None:
            raise ProductNotFoundException(product.id)

        if has_inventory(db=db,product_id=product.id):
            raise ProductHasInventoryException(product.id)

        if has_order(db=db,product_id=product.id):
            raise ProductHasOrderException(product.id)

        return delete_product(
            db=db,
            product=product
        )
