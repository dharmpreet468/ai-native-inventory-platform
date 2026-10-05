from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import WarehouseNotFoundException
from app.models.warehouse import Warehouse
from app.schemas.warehouse import WarehouseCreate,WarehouseResponse,WarehouseUpdate


from app.services.warehouse_services import(
    get_all_warehouses_service,
    get_warehouse_by_id_service,
    create_warehouse_service,
    update_warehouse_service,
    delete_warehouse_service
)


router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"]
)

@router.get("/", response_model=list[WarehouseResponse])
def get_warehouses(db:Session=Depends(get_db)):
    return get_all_warehouses_service(db=db)

@router.get("/{warehouse_id}", response_model=WarehouseResponse)
def get_warehouse(
    warehouse_id:int,
    db:Session=Depends(get_db)
    ):
        warehouse = get_warehouse_by_id_service(
            db=db,
            warehouse_id = warehouse_id
        )

        return warehouse

@router.post("/",response_model=WarehouseResponse)
def create_warehouse(
    warehouse:WarehouseCreate,
    db:Session=Depends(get_db)
):
    new_warehouse = create_warehouse_service(
        db=db,
        name=warehouse.name,
        location=warehouse.location
    )

    db.commit()
    db.refresh(new_warehouse)

    return new_warehouse

@router.put("/{warehouse_id}", response_model=WarehouseResponse)
def update_product_put(
    warehouse_id:int,
    warehouse:WarehouseCreate,
    db:Session=Depends(get_db)
):
    updates = warehouse.model_dump()

    updated_warehouse = update_warehouse_service(
        db=db,
        warehouse_id=warehouse_id,
        update=updates
    )

    db.commit()
    db.refresh(updated_warehouse)

    return updated_warehouse

@router.patch("/{warehouse_id}", response_model=WarehouseResponse)
def update_product_patch(
    warehouse_id:int,
    warehouse:WarehouseUpdate,
    db:Session=Depends(get_db)
):
    updates = warehouse.model_dump(exclude_unset=True)

    updated_warehouse = update_warehouse_service(
        db=db,
        warehouse_id=warehouse_id,
        update=updates
    )

    db.commit()
    db.refresh(updated_warehouse)

    return updated_warehouse

@router.delete("/{product_id}", status_code=204)
def delete_product(
    warehouse_id: int,
    db:Session=Depends(get_db)
):
    warehouse = get_warehouse_by_id_service(
        db=db,
        warehouse_id=warehouse_id
    )
    delete_warehouse_service(
        db=db,
        warehouse=warehouse
    )
    db.commit()
