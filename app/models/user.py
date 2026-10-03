from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column

from app.models.base import Base

class User(Base):
    __tablename__ = "user"
    
    id:Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )
    
    username:Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    
    email:Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_hash:Mapped[str] = mapped_column(String(255),nullable=False)
    role:Mapped[str] = mapped_column(String(50),nullable=False, default="employee")