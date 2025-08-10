from pydantic import EmailStr, BaseModel, ConfigDict
from uuid import UUID


class AddressCreate(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    phone_number: str
    street: str
    house_number: str
    postal_code: str
    city: str

class AddressResponse(AddressCreate):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
