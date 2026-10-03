from pydantic import BaseModel, ConfigDict, Field

class OrderCreate(BaseModel):
    product_id:int
    quantity:int = Field(gt=0)
    
class OrderResponse(BaseModel):
    id:int
    product_id:int
    quantity:int
    status:str
    
    model_config = ConfigDict(from_attributes=True)