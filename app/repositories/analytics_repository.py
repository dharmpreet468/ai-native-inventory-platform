from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.inventory import Inventory
from app.models.order import Order

def get_inventory_summary(db:Session):
    
    total_products = db.query(func.count(Product.id)).scalar() or 0
    
    total_warehouses = db.query(func.count(Warehouse.id)).scalar() or 0
    
    total_inventory_units = (
        db.query(func.coalesce(func.sum(Inventory.quantity),0))
        .scalar() or 0
    )
    total_orders = db.query(func.count(Order.id)).scalar() or 0
    
    total_order_units = (
        db.query(func.coalesce(func.sum(Order.quantity),0))
        .scalar() or 0
    )
    
    total_inventory_value = (
        db.query(
            func.coalesce(
                func.sum(Inventory.quantity * Product.price),0
            )
        )
        .join(Product, Product.id == Inventory.product_id)
        .scalar() or 0
    )
    
    return {
        "total_products": total_products,
        "total_warehouses": total_warehouses,
        "total_inventory_units": total_inventory_units,
        "total_orders": total_orders,
        "total_order_units": total_order_units,
        "total_inventory_value": total_inventory_value,
    }


def get_low_stock_inventory(db: Session, threshold: int = 20):
    return (
        db.query(
            Inventory.product_id.label("product_id"),
            Inventory.warehouse_id.label("warehouse_id"),
            Inventory.quantity.label("quantity"),
            Product.name.label("product_name"),
            Warehouse.name.label("warehouse_name"),
        )
        .join(Product, Inventory.product_id == Product.id)
        .join(Warehouse, Inventory.warehouse_id == Warehouse.id)
        .filter(Inventory.quantity <= threshold)
        .all()
    )