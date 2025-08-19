from pydantic import EmailStr, BaseModel, ConfigDict
from uuid import UUID
from typing import Optional


class AddressCreate(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    phone_number: str
    street: str
    house_number: str
    postal_code: str
    city: str

class AddressUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None

class AddressResponse(AddressCreate):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
