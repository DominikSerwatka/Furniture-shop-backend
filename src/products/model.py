from pydantic import BaseModel, ConfigDict
from uuid import UUID


class ProductCreate(BaseModel):
    name: str
    price: int
    description: str
    picture: str
    space: str
    material: str
    collection: str

class ProductResponse(ProductCreate):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
