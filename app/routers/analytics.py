from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.analytics import (
    InventorySummaryResponse,
    LowStockItem,
    InventoryInsight
)
from app.services.analytics_services import (
    get_inventory_summary_service,
    get_low_stock_inventory_service,
    get_inventory_insight_service
)
router = APIRouter(
    prefix = "/analytics",
    tags=["Analytics"]
)

@router.get("/summary",response_model=InventorySummaryResponse)
def get_inventory_summary(
    db:Session=Depends(get_db)
):
    return get_inventory_summary_service(db=db)

@router.get("/low-stock",response_model=list[LowStockItem])
def get_low_stock_inventory(
    db:Session=Depends(get_db),
    threshold: int = 20
):
    return get_low_stock_inventory_service(db=db, threshold=threshold)

@router.get("/inventory-insights",response_model=list[InventoryInsight])
def get_inventory_insights(
    db:Session=Depends(get_db),
    threshold: int = 20
):
    return get_inventory_insight_service(db=db, threshold=threshold)

