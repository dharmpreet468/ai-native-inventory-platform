from pydantic import BaseModel, ConfigDict

class WarehouseCreate(BaseModel):
    name : str
    location: str
    
class WarehouseResponse(BaseModel):
    id : int
    name : str
    location: str
    
config_model = ConfigDict(from_attributes=True)