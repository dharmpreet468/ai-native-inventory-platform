from pydantic import BaseModel, ConfigDict

class ProductCreate(BaseModel):
    name : str
    price : float
    category : str
class ProductUpdate(BaseModel):
    name : str | None = None
    price : float | None = None
    category : str | None = None

class ProductResponse(BaseModel):
    id : int
    name : str
    price : float
    category : str

    model_config = ConfigDict(from_attributes=True)
