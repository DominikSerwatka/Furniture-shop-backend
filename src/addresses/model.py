from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


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
    name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    street: str | None = None
    house_number: str | None = None
    postal_code: str | None = None
    city: str | None = None


class AddressResponse(AddressCreate):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
