from pydantic import BaseModel, ConfigDict

class ProductCreate(BaseModel):
    name : str
    price : float
    category : str | None = None
    
class ProductResponse(BaseModel):
    id : int
    name : str
    price : float
    category : str | None = None
    
model_config = ConfigDict(from_attributes=True)