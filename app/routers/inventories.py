from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Core
from app.core.database import get_db

# Schemas
from app.schemas.inventory import InventoryCreate,InventoryResponse,InventoryUpdate

# Services
from app.services.inventory_services import (
    get_all_inventory_service,
    get_inventory_by_id_service,
    create_or_update_inventory_service,
    update_inventory_service,
    delete_inventory_service
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
        return get_inventory_by_id_service(
            db=db,
            inventory_id=inventory_id
        )

@router.post("/",response_model=InventoryResponse)
def create_inventory(
    inventory:InventoryCreate,
    db:Session=Depends(get_db)
):
    new_inventory = create_or_update_inventory_service(
        db=db,
        product_id=inventory.product_id,
        warehouse_id=inventory.warehouse_id,
        quantity=inventory.quantity
    )

    db.commit()
    db.refresh(new_inventory)

    return new_inventory

@router.put("/{inventory_id}",response_model=InventoryResponse)
def update_inventory_put(
    inventory_id:int,
    inventory:InventoryCreate,
    db:Session=Depends(get_db)
):
    updates = inventory.model_dump()
    updated_inventory = update_inventory_service(
        db=db,
        inventory_id=inventory_id,
        update=updates
    )

    db.commit()
    db.refresh(updated_inventory)

    return updated_inventory

@router.patch("/{inventory_id}",response_model=InventoryResponse)
def update_inventory_patch(
    inventory_id:int,
    inventory:InventoryUpdate,
    db:Session=Depends(get_db)
):
    updates = inventory.model_dump(exclude_unset=True)
    updated_inventory = update_inventory_service(
        db=db,
        inventory_id=inventory_id,
        update=updates
    )

    db.commit()
    db.refresh(updated_inventory)

    return updated_inventory

@router.delete("/{inventory_id}",status_code=204)
def delete_inventory(
    inventory_id:int,
    db:Session=Depends(get_db)
):
    delete_inventory_service(
        db=db,
        inventory_id=inventory_id
    )

    db.commit()
