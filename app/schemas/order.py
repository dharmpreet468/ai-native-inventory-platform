from pydantic import BaseModel, ConfigDict, Field

class OrderCreate(BaseModel):
    product_id:int
    quantity:int = Field(gt=0)

class OrderUpdate(BaseModel):
    product_id: int | None = None
    quantity:int | None = Field(default= None,gt=0)

class OrderResponse(BaseModel):
    id:int
    product_id:int
    quantity:int
    status:str

    model_config = ConfigDict(from_attributes=True)
