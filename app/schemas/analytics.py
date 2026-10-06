from pydantic import BaseModel

class InventorySummaryResponse(BaseModel):
    total_products:int
    total_warehouses:int
    total_inventory_units:int
    total_orders:int
    total_order_units:int
    total_inventory_value:float
    
class LowStockItem(BaseModel):
    product_id:int
    warehouse_id:int
    product_name:str
    warehouse_name:str
    quantity:int
    threshold:int
    
class InventoryInsight(BaseModel):
    product_id:int
    warehouse_id:int
    product_name:str
    warehouse_name:str
    quantity:int
    threshold:int
    severity:str
    recommendation:str