from sqlalchemy.orm import Session

from app.models.warehouse import Warehouse
from app.models.inventory import Inventory

def get_all_warehouses(db:Session):
    return db.query(Warehouse).all()

def get_warehouse_by_id(
    db:Session,
    warehouse_id:int
):
    return db.query(Warehouse).filter(
        Warehouse.id == warehouse_id
    ).first()

def add_warehouse(
    db:Session,
    warehouse:Warehouse
):
    db.add(warehouse)

    return warehouse

def update_warehouse(
    warehouse:Warehouse,
    update:dict
):
    for field,value in update.items():
        setattr(warehouse,field,value)

    return warehouse

def delete_warehouse(
    db:Session,
    warehouse:Warehouse
):
    db.delete(warehouse)

def has_inventory(
    db:Session,
    warehouse_id:int
):
    return db.query(Inventory).filter(
        Inventory.warehouse_id == warehouse_id
    ).first() is not None
