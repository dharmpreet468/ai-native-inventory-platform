from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.product import Product

class Order(Base):
    __tablename__ = "orders"
    
    id:Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )
    
    product_id:Mapped[int]=mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )
    
    quantity:Mapped[int]=mapped_column(
        nullable=False
    )
    
    status:Mapped[str]=mapped_column(
        String(50),
        nullable=False,
        default="CONFIRMED"
    )
    
    product:Mapped["Product"] = relationship()
    