from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    name: str
    price: int
    description: str
    sku: str
    picture: str
    space: str
    material: str
    collection: str
    is_active: bool


class ProductResponse(ProductCreate):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
