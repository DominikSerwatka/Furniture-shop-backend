import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer, Text, DateTime, func

from src.database.core import Base
from sqlalchemy import Column

class Product(Base):
    __tablename__ = 'products'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    picture = Column(String(512), nullable=False)
    space = Column(String(64), nullable=False)
    material = Column(String(64), nullable=False)
    collection = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
