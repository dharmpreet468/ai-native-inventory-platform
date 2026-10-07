from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

#  Core
from app.core.database import engine

#  Models
from app.models.base import Base
from app.models.order import Order
from app.models.order_allocation import OrderAllocation

#  Routers
from app.routers.products import router as products_router
from app.routers.warehouses import router as warehouses_router
from app.routers.inventories import router as inventories_router
from app.routers.orders import router as orders_router
from app.routers.analytics import router as analytics_router

# Centeralized Error Handler
from app.core.exceptions import (
    ProductNotFoundException,
    WarehouseNotFoundException,
    InventoryNotFoundException,
    OrderNotFoundException,
    InsufficientInventory,
    DuplicateProductException,
    DuplicateWarehouseException,
    ProductHasInventoryException,
    ProductHasOrderException,
    WarehouseHasInventoryException,
    InventoryAlreadyExistsException,
    CancelledOrderException,
    OrderAlreadyConfirmedException

)

app = FastAPI(
    title= "AI Native Inventory Management Platform",
    version= "1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)
app.include_router(products_router)
app.include_router(warehouses_router)
app.include_router(inventories_router)
app.include_router(orders_router)
app.include_router(analytics_router)

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

# Centralised Error Handling

@app.exception_handler(ProductNotFoundException)
async def product_not_found_handler(
    request: Request,
    exc: ProductNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content = {
            "error" : "PRODUCT_NOT_FOUND",
            "message" : str(exc),
            "product_id":exc.product_id
        }
    )

@app.exception_handler(WarehouseNotFoundException)
async def warehouse_not_found_handler(
    request: Request,
    exc: WarehouseNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content = {
            "error" : "WAREHOUSE_NOT_FOUND",
            "message" : str(exc),
            "warehouse_id": exc.warehouse_id
        }
    )

@app.exception_handler(InventoryNotFoundException)
async def inventory_not_found_handler(
    request: Request,
    exc: InventoryNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content = {
            "error" : "INVENTORY_NOT_FOUND",
            "message" : str(exc),
            "inventory_id": exc.inventory_id
        }
    )

@app.exception_handler(OrderNotFoundException)
async def order_not_found_handler(
    request: Request,
    exc: OrderNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content = {
            "error" : "INVENTORY_NOT_FOUND",
            "message" : str(exc),
            "inventory_id": exc.order_id
        }
    )

@app.exception_handler(InsufficientInventory)
async def insufficent_inventory_handler(
    request: Request,
    exc:InsufficientInventory
):
    return JSONResponse(
        status_code= 409,
        content = {
            "error":"INSUFFICIENT_INVENTORY",
            "message": str(exc),
            "product_id":exc.product_id,
            "requested":exc.requested,
            "available":exc.available
        }
    )

@app.exception_handler(ProductHasInventoryException)
async def product_has_inventory_handler(
    request: Request,
    exc:ProductHasInventoryException
):
    return JSONResponse(
        status_code= 409,
        content = {
            "error":"PRODUCT_HAS_INVENTORY",
            "message": str(exc),
            "product_id":exc.product_id
        }
    )

@app.exception_handler(ProductHasOrderException)
async def product_has_order_handler(
    request: Request,
    exc:ProductHasOrderException
):
    return JSONResponse(
        status_code= 409,
        content = {
            "error":"PRODUCT_HAS_ORDER",
            "message": str(exc),
            "product_id":exc.product_id
        }
    )

@app.exception_handler(WarehouseHasInventoryException)
async def warehouse_has_inventory_handler(
    request: Request,
    exc:WarehouseHasInventoryException
):
    return JSONResponse(
        status_code= 409,
        content = {
            "error":"WAREHOUSE_HAS_INVENTORY",
            "message": str(exc),
            "warehouse_id":exc.warehouse_id
        }
    )

@app.exception_handler(InventoryAlreadyExistsException)
async def inventory_already_existed_handler(
    request: Request,
    exc:InventoryAlreadyExistsException
):
    return JSONResponse(
        status_code= 409,
        content = {
            "error":"INVENTORY_ALREADY_EXISTED",
            "message": str(exc),
            "product_id":exc.product_id,
            "warehouse_id":exc.warehouse_id
        }
    )

@app.exception_handler(CancelledOrderException)
async def cancelled_order_handler(
    request: Request,
    exc:CancelledOrderException
):
    return JSONResponse(
        status_code= 409,
        content = {
            "error":"ORDER_CANCELLED_ALREADY",
            "message": str(exc),
            "order_id":exc.order_id
        }
    )

@app.exception_handler(OrderAlreadyConfirmedException)
async def order_already_confirmed_handler(
    request: Request,
    exc:OrderAlreadyConfirmedException
):
    return JSONResponse(
        status_code= 409,
        content = {
            "error":"ORDER_ALREADY_CONFIRMED",
            "message": str(exc),
            "order_id":exc.order_id
        }
    )

