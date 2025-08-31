import uuid

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID

from src.database.core import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return (
            f"<User(email='{self.email}', name={self.name}, last_name={self.last_name}, created_at={self.created_at})>"
        )
