from uuid import uuid4
from sqlalchemy import String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Float)
    available: Mapped[bool] = mapped_column(Boolean, default=True)

    def __init__(self, **kwargs):
        self.id = uuid4().hex
        super().__init__(**kwargs)