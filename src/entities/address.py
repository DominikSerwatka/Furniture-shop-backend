import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID

from src.database.core import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    street = Column(String, nullable=False)
    house_number = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    city = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return (
            f"<Address(name='{self.name}', last_name='{self.last_name}',"
            f" email='{self.email}', phone_number='{self.phone_number}',"
            f" street='{self.street}', house_number='{self.house_number}',"
            f" postal_code='{self.postal_code}', city='{self.city}')>"
        )
