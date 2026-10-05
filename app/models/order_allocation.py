from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.order import Order
    from app.models.inventory import Inventory

class OrderAllocation(Base):
    __tablename__ = "order_allocations"

    id:Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    order_id:Mapped[int]=mapped_column(
        ForeignKey("orders.id"),
        nullable=False
    )

    inventory_id:Mapped[int]=mapped_column(
        ForeignKey("Inventory.id"),
        nullable=False
    )

    quantity:Mapped[int]=mapped_column(
        nullable=False
    )

    product:Mapped["Order"] = relationship()

