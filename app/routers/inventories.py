from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Core
from app.core.database import get_db

# Schemas
from app.schemas.inventory import InventoryCreate,InventoryResponse

# Services
from app.services.inventory_services import (
    get_all_inventory_service,
    get_inventory_by_id_service,
    create_or_update_inventory_service
)

router = APIRouter(
    prefix="/inventories",
    tags=["Inventories"]
)

@router.get("/", response_model=list[InventoryResponse])
def get_inventories(db:Session=Depends(get_db)):
    return get_all_inventory_service(db=db)

@router.get("/{inventory_id}",response_model=InventoryResponse)
def get_inventory(
    inventory_id:int,
    db:Session=Depends(get_db)
    ):
        inventory = get_inventory_by_id_service(
            db=db,
            inventory_id=inventory_id
        )
        
        if inventory is None:
            raise HTTPException(
                status_code=404,
                detail="Inventory not found"
            )
        
        return inventory
    
@router.post("/",response_model=InventoryResponse)
def create_inventory(
    product_id : int, warehouse_id:int,
    inventory:InventoryCreate,
    db:Session=Depends(get_db)
):
    try:
        new_inventory = create_or_update_inventory_service(
            db=db,
            product_id=product_id,
            warehouse_id=warehouse_id,
            quantity=inventory.quantity
        )
        
        db.commit()
        db.refresh(new_inventory)
    
        return new_inventory
    
    except ValueError as e:
        db.rollback()
        
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:
        db.rollback()
        
        raise HTTPException(
            status_code=500,
            detail="Failed to create inventory"
        )