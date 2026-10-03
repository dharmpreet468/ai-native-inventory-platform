from fastapi import FastAPI

#  Core
from app.core.database import engine

#  Models
from app.models.base import Base

#  Routers
from app.routers.products import router as products_router
from app.routers.warehouses import router as warehouses_router
from app.routers.inventories import router as inventories_router

app = FastAPI(
    title= "AI Native Inventory Management Platform",
    version= "1.0.0"
)

Base.metadata.create_all(bind=engine)
app.include_router(products_router)
app.include_router(warehouses_router)
app.include_router(inventories_router)

@app.get("/")
def root():
    return {
        "message":"AI Native Inventory Management API is running..."
    }

@app.get("/health")
def health_check():
    try:
        with engine.connect():
            return{
                "status":"healthy",
                "database":"connected",
            }
    except Exception as e:
        return{
            "status":"unhealthy",
            "database":"disconnected",
            "error":str(e)
        }
