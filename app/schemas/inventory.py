from pydantic import BaseModel, ConfigDict, Field

class InventoryCreate(BaseModel):
    product_id : int
    warehouse_id : int
    quantity : int = Field(ge=0)

class InventoryUpdate(BaseModel):
    product_id:int | None=None
    warehouse_id:int | None=None
    quantity:int | None= Field(default=None, ge=0)

class InventoryResponse(BaseModel):
    id : int
    product_id : int
    warehouse_id : int
    quantity : int

    model_config = ConfigDict(from_attributes=True)


