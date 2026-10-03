from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.warehouse import Warehouse
from app.schemas.warehouse import WarehouseCreate,WarehouseResponse


router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"]
) 

@router.get("/", response_model=list[WarehouseResponse])
def get_warehouses(db:Session=Depends(get_db)):
    warehouses = db.query(Warehouse).all()
    return warehouses

@router.get("/{warehouse_id}", response_model=WarehouseResponse)
def get_warehouse(
    warehouse_id:int,
    db:Session=Depends(get_db)
    ):
        warehouse = db.query(Warehouse).filter(Warehouse.id==warehouse_id).first()
        
        if warehouse is None:
            raise HTTPException(
                status_code=404,
                detail="Warehouse not found"
            )
        return warehouse

@router.post("/",response_model=WarehouseResponse)
def create_warehouse(
    warehouse:WarehouseCreate,
    db:Session=Depends(get_db)
):
    new_warehouse = Warehouse(
        name = warehouse.name,
        location = warehouse.location
    )
    
    db.add(new_warehouse)
    db.commit()
    db.refresh(new_warehouse)
    
    return new_warehouse
