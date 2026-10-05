from pydantic import BaseModel, ConfigDict

class WarehouseCreate(BaseModel):
    name : str
    location: str

class WarehouseUpdate(BaseModel):
    name : str | None = None
    location: str | None = None

class WarehouseResponse(BaseModel):
    id : int
    name : str
    location: str

    model_config = ConfigDict(from_attributes=True)
