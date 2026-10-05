from typing import TYPE_CHECKING

from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.inventory import Inventory

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index= True
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)

    inventory: Mapped[list["Inventory"]] = relationship(back_populates="product")

