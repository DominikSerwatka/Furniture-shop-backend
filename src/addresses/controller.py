from uuid import UUID

from fastapi import APIRouter
from starlette import status

from src.addresses.model import AddressCreate, AddressResponse, AddressUpdate
from src.addresses.service import (
    create_address,
    delete_address_by_id,
    get_address_by_id,
    get_addresses,
    update_address,
)
from src.auth.service import CurrentUser
from src.database.core import DbSession

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address_controller(db: DbSession, address: AddressCreate, current_user: CurrentUser):
    return create_address(current_user, db, address)


@router.get("/", response_model=list[AddressResponse])
def get_addresses_controller(db: DbSession, current_user: CurrentUser):
    return get_addresses(current_user, db)


@router.get("/{address_id}", response_model=AddressResponse)
def get_address_controller(db: DbSession, address_id: UUID, current_user: CurrentUser):
    return get_address_by_id(current_user, db, address_id)


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address_controller(db: DbSession, address_id: UUID, current_user: CurrentUser):
    return delete_address_by_id(current_user, db, address_id)


@router.put("/{address_id}", response_model=AddressResponse)
def update_address_controller(
    db: DbSession, address_id: UUID, current_user: CurrentUser, address: AddressUpdate
):
    return update_address(current_user, db, address_id, address)
