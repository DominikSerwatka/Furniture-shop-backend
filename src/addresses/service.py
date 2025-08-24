import logging
from uuid import UUID

from sqlalchemy.orm import Session

from src.addresses.model import AddressCreate, AddressUpdate
from src.auth.model import TokenData
from src.entities.address import Address
from src.exceptions import AddressCreationError, AddressNotFoundError


def create_address(current_user: TokenData, db: Session, address: AddressCreate) -> Address:
    try:
        new_address = Address(**address.model_dump())
        new_address.user_id = current_user.get_uuid()
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
        logging.info(f"Create new address for user: {current_user.get_uuid()}")
        return new_address
    except Exception as e:
        logging.error(
            f"Failed to create address for user {current_user.get_uuid()}. Error: {str(e)}"
        )
        raise AddressCreationError(str(e)) from None


def get_addresses(current_user: TokenData, db: Session) -> list[Address]:
    addresses = db.query(Address).filter(Address.user_id == current_user.get_uuid()).all()
    logging.info(f"Retrieved {len(addresses)} for user: {current_user.get_uuid()}")
    return addresses


def get_address_by_id(current_user: TokenData, db: Session, address_id: UUID) -> Address:
    address = (
        db.query(Address)
        .filter(Address.id == address_id)
        .filter(Address.user_id == current_user.get_uuid())
        .one_or_none()
    )
    if not address:
        logging.warning(f"Address {address_id} not found for user {current_user.get_uuid()}")
        raise AddressNotFoundError(address_id)
    logging.info(f"Retrieved address {address_id} for user {current_user.get_uuid()}")
    return address


def delete_address_by_id(current_user: TokenData, db: Session, address_id: UUID):
    address = get_address_by_id(current_user, db, address_id)
    if address:
        db.delete(address)
        db.commit()
        logging.info(f"Deleted address {address_id} for user {current_user.get_uuid()}")


def update_address(
    current_user: TokenData, db: Session, address_id: UUID, address_update: AddressUpdate
) -> Address:
    address = get_address_by_id(current_user, db, address_id)
    for field, value in address_update.model_dump(exclude_unset=True).items():
        setattr(address, field, value)
    db.commit()
    db.refresh(address)
    logging.info(f"Update address {address_id} for user {current_user.get_uuid()}")
    return address
