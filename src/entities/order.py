import uuid
from enum import Enum

from sqlalchemy.types import JSON as SA_JSON
from sqlalchemy import Enum as SAEnum, String, DateTime, func, CheckConstraint, Index, Text, Integer

from sqlalchemy import Column, UUID, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSONB

from src.database.core import Base

DeliveryJson = SA_JSON().with_variant(JSONB, "postgresql")

class OrderStatus(str, Enum):
    PLACED = "PLACED"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    RETURNED = "RETURNED"


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    delivery_address_snapshot = Column(DeliveryJson, nullable=True)

    delivery_address_id = Column(
        UUID(as_uuid=True),
        ForeignKey("addresses.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    items_total = Column(Numeric(10, 2), nullable=False)
    delivery_fee = Column(Numeric(10, 2), nullable=False, server_default="0")
    discount_total = Column(Numeric(10, 2), nullable=False, server_default="0")
    grand_total = Column(Numeric(10, 2), nullable=False)
    status = Column(SAEnum(OrderStatus), nullable=False, server_default=OrderStatus.PLACED.value)
    payment_method = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    paid_at = Column(DateTime(timezone=True), nullable=True)
    shipped_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint("items_total >= 0", name="orders_items_total_nonneg"),
        CheckConstraint("delivery_fee >= 0", name="orders_delivery_fee_nonneg"),
        CheckConstraint("discount_total >= 0", name="orders_discount_total_nonneg"),
        CheckConstraint("grand_total >= 0", name="orders_grand_total_nonneg"),
        Index("ix_orders_user_created", "user_id", "created_at"),
        Index("ix_orders_status_created", "status", "created_at"),
    )

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    sku_snapshot = Column(String, nullable=False)
    name_snapshot = Column(String(255), nullable=False)
    image_url_snapshot = Column(Text, nullable=True)
    unit_price_snapshot = Column(Numeric(10, 2), nullable=False)
    qty = Column(Integer, nullable=False, server_default="1")
    line_total = Column(Numeric(10,2), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        CheckConstraint("qty > 0", name="order_items_qty_positive"),
        CheckConstraint("unit_price_snapshot >= 0", name="order_items_price_nonneg"),
        CheckConstraint("line_total >= 0", name="order_items_total_nonneg"),
    )