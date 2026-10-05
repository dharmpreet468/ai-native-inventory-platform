from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.order import Order
from app.models.inventory import Inventory

def get_all_products(db:Session):
    return db.query(Product).all()

def get_products_by_id(
    db:Session,
    product_id: int
):
    return db.query(Product).filter(
        Product.id == product_id
    ).first()

def add_product(
    db:Session,
    product:Product
):
    db.add(product)

    return product

def update_product(
    product:Product,
    update:dict
):
    for field, value in update.items():
        setattr(product,field,value)

    return product

def delete_product(
    db:Session,
    product:Product
):
    db.delete(product)

def has_inventory(
    db:Session,
    product_id:int
):
    return db.query(Inventory).filter(
        Inventory.product_id == product_id
    ).first() is not None

def has_order(
    db: Session,
    product_id: int
):
    return db.query(Order).filter(
        Order.product_id == product_id
    ).first() is not None
