from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.inventory import Inventory

class Warehouse(Base):
    __tablename__= "warehouses"

    id:Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name:Mapped[str] = mapped_column(String(100), nullable=False)
    location:Mapped[str] = mapped_column(String(200), nullable=False)

    inventory:Mapped[list["Inventory"]] = relationship(back_populates="warehouse")
