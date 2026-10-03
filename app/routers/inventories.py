from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.schemas.inventory import InventoryCreate,InventoryResponse


router = APIRouter(
    prefix="/inventories",
    tags=["Inventories"]
)

@router.get("/", response_model=list[InventoryResponse])
def get_inventories(db:Session=Depends(get_db)):
    inventories = db.query(Inventory).all();
    return inventories

@router.get("/{inventory_id}",response_model=InventoryResponse)
def get_inventory(
    inventory_id:int,
    db:Session=Depends(get_db)
    ):
        inventory = db.query(Inventory).filter(
            Inventory.id == inventory_id
        ).first()
        
        if inventory is None:
            raise HTTPException(
                status_code = 404,
                detail="Inventory not found"
            )
        return inventory
    
@router.post("/",response_model=InventoryResponse)
def create_inventory(
    product_id: int, warehouse_id:int,
    inventory:InventoryCreate,
    db:Session=Depends(get_db)
):
    #  Checking for existing product data
    product = db.query(Product).filter(Product.id==product_id).first()
    
    if product is None:
        raise HTTPException(
            status_code= 404,
            detail="Product not found"
        )
        
    #  Checking for existing warehouse data
    warehouse = db.query(Warehouse).filter(Warehouse.id==warehouse_id).first()
    
    if warehouse is None:
        raise HTTPException(
            status_code= 404,
            detail="Warehouse not found"
        )
    
    #  Checking for existing inventory data
    existing_inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id,
        Inventory.warehouse_id == warehouse_id
    ).first()
    
    if existing_inventory:
        existing_inventory.quantity += inventory.quantity
        
        db.commit()
        db.refresh(existing_inventory)
        
        return existing_inventory 
        
    new_inventory = Inventory(
        product_id = inventory.product_id,
        warehouse_id = inventory.warehouse_id,
        quantity = inventory.quantity
    )
    
    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)
    
    return new_inventory