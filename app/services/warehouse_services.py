from sqlalchemy.orm import Session

from app.core.exceptions import WarehouseNotFoundException,WarehouseHasInventoryException
from app.models.warehouse import Warehouse
from app.repositories.warehouse_repository import (
    get_all_warehouses,
    get_warehouse_by_id,
    update_warehouse,
    delete_warehouse,
    add_warehouse,
    has_inventory
)

def get_all_warehouses_service(db:Session):
    return get_all_warehouses(db=db)

def get_warehouse_by_id_service(
    db:Session,
    warehouse_id:int
):
    warehouse = get_warehouse_by_id(
        db=db,
        warehouse_id=warehouse_id
    )

    if warehouse is None:
        raise WarehouseNotFoundException(warehouse_id)

    return warehouse

def create_warehouse_service(
    db:Session,
    name:str,
    location:str,
):
    warehouse = Warehouse(
        name = name,
        location = location
    )

    return add_warehouse(
        db=db,
        warehouse=warehouse
    )


def update_warehouse_service(
    db:Session,
    warehouse_id:int,
    update:dict
):
    warehouse = get_warehouse_by_id(
        db=db,
        warehouse_id=warehouse_id
    )

    if warehouse is None:
        raise WarehouseNotFoundException(warehouse_id)

    return update_warehouse(
        warehouse=warehouse,
        update=update
    )

def delete_warehouse_service(
        db:Session,
        warehouse:Warehouse
    ):
        if warehouse is None:
            raise ProductNotFoundException(warehouse.id)

        if has_inventory(db=db,warehouse_id=warehouse.id):
                raise WarehouseHasInventoryException(warehouse.id)
        return delete_warehouse(
            db=db,
            warehouse=warehouse
        )
