import uuid

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID

from src.database.core import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    sku = Column(String(64), nullable=True, unique=True, index=True)
    picture = Column(String(512), nullable=False)
    space = Column(String(64), nullable=False)
    material = Column(String(64), nullable=False)
    collection = Column(String(64), nullable=False)
    is_active = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
