from fastapi import APIRouter

from src.auth.service import CurrentUser
from src.database.core import DbSession
from src.users.model import UserResponse, PasswordChange
from src.users.service import get_user_by_id
from starlette import status

router = APIRouter(
    prefix='/users',
    tags=["Users"]
)


@router.get("/me", response_model=UserResponse)
def get_current_user(current_user: CurrentUser, db: DbSession):
    return get_user_by_id(db, current_user.get_uuid())

@router.put("/change-password", status_code=status.HTTP_200_OK)
def change_password(password_change: PasswordChange, db: DbSession, current_user: CurrentUser):
    change_password(db, current_user.get_uuid(), password_change)