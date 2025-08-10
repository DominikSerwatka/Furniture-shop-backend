from fastapi import HTTPException


class AddressError(HTTPException):
    """Base exception for address-related errors"""
    pass


class AddressCreationError(AddressError):
    def __init__(self, error: str):
        message = f"Failed to create address: {error}"
        super().__init__(status_code=500, detail=message)

class AddressNotFoundError(AddressError):
    def __int__(self, address_id=None):
        message = "Address not found" if address_id is None else f"Address with id {address_id} not found"
        super().__init__(status_code=404, detail=message)


class UserError(HTTPException):
    """Base exception for user-related errors"""
    pass

class UserNotFoundError(UserError):
    def __init__(self, user_id=None):
        message = f"User not found" if user_id is None else f"User with id {user_id} not found"
        super().__init__(status_code=404, detail=message)

class UserInvalidPassword(UserError):
    def __init__(self):
        message = f"Current password is incorrect"
        super().__init__(status_code=401, detail=message)

class UserPasswordMismatchError(UserError):
    def __init__(self):
        message = f"New password do not match"
        super().__init__(status_code=400, detail=message)

class AuthenticationError(HTTPException):
    message = "Could not validate user"
    def __init__(self):
        super().__init__(status_code=401, detail=AuthenticationError.message)
