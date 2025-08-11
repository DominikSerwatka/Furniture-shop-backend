from fastapi import APIRouter, Depends, Request

from src.auth.service import register_user, login_for_access_token, refresh_access_token, logout
from src.database.core import DbSession
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from src.auth.model import RegisterUserRequest, Token

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user_controller(db: DbSession, register_user_request: RegisterUserRequest):
    register_user(db, register_user_request)


@router.post("/token")
async def login_for_access_token_controller(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession):
    return login_for_access_token(form_data, db)


@router.post("/refresh")
async def refresh_access_token_controller(request: Request, db: DbSession):
    return refresh_access_token(request, db)


@router.post("/logout")
async def logout_controller(request: Request, db: DbSession):
    return logout(request, db)