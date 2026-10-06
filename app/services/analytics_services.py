from sqlalchemy.orm import Session

from app.repositories.analytics_repository import (
    get_inventory_summary,
    get_low_stock_inventory
)

def get_inventory_summary_service(db:Session):
    return get_inventory_summary(db=db)

def get_low_stock_inventory_service(db:Session, threshold:int = 20):
    inventory = get_low_stock_inventory(
        db=db, 
        threshold=threshold
        )
    
    return [
        {
            "product_id": item._mapping["product_id"],
            "warehouse_id": item._mapping["warehouse_id"],
            "product_name": item._mapping["product_name"],
            "warehouse_name": item._mapping["warehouse_name"],
            "quantity": item._mapping["quantity"],
            "threshold": threshold,
        }  for item in inventory
    ]

def get_inventory_insight_service(
    db:Session,
    threshold:int=20
):
    inventory = get_low_stock_inventory(
        db=db,
        threshold=threshold
    )
    
    insights = []
    
    for item in inventory:
        row = item._mapping
    
        quantity = row["quantity"]
        
        if quantity == 0:
            severity = "CRITICAL"
            recommendation = (
                f"Product {row["product_name"]} is out of stock "
                f"at {row["warehouse_name"]}. Replenishment is required."
            )
        else:
            severity = "WARNING"
            recommendation = (
                f"Product {row["product_name"]} is low in stock "
                f"at {row["warehouse_name"]}. Consider Replenishment."
            )
    
    insights.append(
        {
            "product_id": row["product_id"],
            "warehouse_id": row["warehouse_id"],
            "product_name": row["product_name"],
            "warehouse_name": row["warehouse_name"],
            "quantity": quantity,
            "threshold": threshold,
            "severity": severity,
            "recommendation": recommendation,
        }

    )
    
    return insights
        
    
