from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.models.product import Product
from app.core.database import get_db
from app.schemas.product import ProductCreate,ProductResponse

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/",response_model=list[ProductResponse])
def get_products(db:Session = Depends(get_db)):
    products = db.query(Product).all()
    
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id:int,
    db:Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id==product_id).first()
    
    if product is None:
        raise HTTPException(
            status_code = 404,
            detail= "Product not found"
        )
    
    return product

@router.post("/",response_model=ProductResponse)
def create_products(
    product:ProductCreate,
    db:Session = Depends(get_db)
    ):
        new_product = Product(
            name = product.name,
            price = product.price,
            category = product.category
        )
    
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        
        return new_product