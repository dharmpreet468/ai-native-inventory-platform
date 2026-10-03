from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.warehouse import Warehouse

class Inventory(Base):
    __tablename__ = "Inventory"
    
    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "warehouse_id",
            name = "uq_product_warehouse"
        ),
    )
    
    id:Mapped[int]=mapped_column(
        primary_key= True,
        index=True
    )
    
    product_id:Mapped[int]=mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )
    
    warehouse_id:Mapped[int]=mapped_column(
        ForeignKey("warehouses.id"),
        nullable=False
    )
    
    
    quantity:Mapped[int]=mapped_column(
        nullable=False,
        default=0
    )
    
    product:Mapped["Product"] = relationship(back_populates="inventory")
    warehouse:Mapped["Warehouse"] = relationship(back_populates="inventory")