from fastapi import APIRouter, Depends, Request
from src.database.core import DbSession
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from src.auth.model import RegisterUserRequest
from model import Token
from service import register_user, login_for_access_token

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user_controller(request: Request, db: DbSession, register_user_request: RegisterUserRequest):
    register_user(db, register_user_request)

@router.post("/token", response_model=Token)
async def login_for_access_token_controller(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession):
    return login_for_access_token(form_data, db)



