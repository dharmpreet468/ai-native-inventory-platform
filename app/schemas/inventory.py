from pydantic import BaseModel, ConfigDict, Field

class InventoryCreate(BaseModel):
    product_id : int
    warehouse_id : int
    quantity : int = Field(ge=0)
    
class InventoryResponse(BaseModel):
    id : int
    product_id : int
    warehouse_id : int
    quantity : int
    
config_model = ConfigDict(from_attributes=True)