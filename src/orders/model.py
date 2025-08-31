from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, EmailStr, condecimal, conint

from src.entities.order import OrderStatus


class AddressSnapshot(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    phone_number: str
    street: str
    house_number: str
    postal_code: str
    city: str


class OrderItemCreate(BaseModel):
    product_id: UUID
    qty: conint(strict=True, gt=0) = 1


class OrderCreate(BaseModel):
    items: list[OrderItemCreate]
    delivery_address_snapshot: AddressSnapshot
    delivery_address_id: UUID | None = None
    delivery_fee: condecimal(max_digits=10, decimal_places=2) = Decimal("0.00")
    discount_total: condecimal(max_digits=10, decimal_places=2) = Decimal("0.00")
    payment_method: str | None = None


class OrderItemResponse(BaseModel):
    id: UUID
    product_id: UUID | None = None
    sku_snapshot: str | None = None
    name_snapshot: str
    image_url_snapshot: str | None = None
    unite_price_snapshot: Decimal
    qty: int
    line_total: Decimal


class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    delivery_address_id: UUID | None = None
    delivery_address_snapshot: AddressSnapshot
    items_total: Decimal
    delivery_fee: Decimal
    discount_total: Decimal
    grand_total: Decimal
    status: OrderStatus
    payment_method: str
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True
