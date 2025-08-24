import logging
import os
import secrets
from datetime import UTC, datetime, timedelta
from typing import Annotated
from uuid import UUID, uuid4

import jwt
from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.auth.model import RegisterUserRequest, Token, TokenData
from src.entities.refresh_token import RefreshToken
from src.entities.user import User
from src.exceptions import AuthenticationError

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def authenticate_user(email: str, password: str, db: Session) -> User | bool:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        logging.warning(f"Failed authentication attempt for email: {email}")
        return False
    return user


def create_access_token(email: str, user_id: UUID, expires_delta: timedelta) -> str:
    encode = {"sub": email, "id": str(user_id), "exp": datetime.now(UTC) + expires_delta}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        return TokenData(user_id=user_id)
    except InvalidTokenError as e:
        logging.warning(f"Token verification failed: {str(e)}")
        raise AuthenticationError() from None


def register_user(db: Session, register_user_request: RegisterUserRequest) -> None:
    try:
        create_user_model = User(
            id=uuid4(),
            email=register_user_request.email,
            name=register_user_request.name,
            last_name=register_user_request.last_name,
            password_hash=get_password_hash(register_user_request.password),
        )
        db.add(create_user_model)
        db.commit()
    except Exception as e:
        logging.error(f"Failed to register user: {register_user_request.email}. Error: {str(e)}")
        db.rollback()
        raise


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> TokenData:
    return verify_token(token)


CurrentUser = Annotated[TokenData, Depends(get_current_user)]


def create_refresh_token(user_id: UUID, days: int = REFRESH_TOKEN_EXPIRE_DAYS):
    jti = secrets.token_hex(16)
    exp = datetime.now(UTC) + timedelta(days=days)
    payload = {"sub": str(user_id), "jti": jti, "exp": exp}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, jti, exp


def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session
) -> JSONResponse:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise AuthenticationError()
    token = create_access_token(user.email, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token, jti, exp = create_refresh_token(user_id=user.id)
    try:
        db.add(RefreshToken(user_id=user.id, jti=jti, expires_at=exp))
        db.commit()
    except Exception as e:
        logging.error(
            f"Failed to login user {user.id}, error with Refresh Token creation, error: {str(e)}"
        )
        db.rollback()
        raise

    response = JSONResponse(content=Token(access_token=token, token_type="bearer").model_dump())
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # True in production (HTTPS)
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        path="/auth",
    )
    return response


def refresh_access_token(request: Request, db: Session):
    token = request.cookies.get("refresh_token")
    if not token:
        raise AuthenticationError()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        raise AuthenticationError() from None

    sub = payload.get("sub")
    jti = payload.get("jti")
    if not sub or not jti:
        raise AuthenticationError()

    refresh_token = db.query(RefreshToken).filter_by(jti=jti, user_id=UUID(sub)).one_or_none()
    if (
        not refresh_token
        or refresh_token.revoked_at
        or refresh_token.expires_at < datetime.now(UTC)
    ):
        raise AuthenticationError()

    refresh_token.revoked_at = datetime.now(UTC)  # rotate old token

    user = db.query(User).with_entities(User.email).filter(User.id == UUID(sub)).scalar()
    if not user:
        raise AuthenticationError()

    access_token = create_access_token(
        user, UUID(sub), timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    new_refresh_token, new_jti, new_exp = create_refresh_token(user_id=UUID(sub))
    try:
        db.add(RefreshToken(user_id=UUID(sub), jti=new_jti, expires_at=new_exp))
        db.commit()
    except Exception as e:
        logging.error(
            f"Failed to refresh token user {UUID(sub)}, "
            f"error with Refresh Token creation, error: {str(e)}"
        )
        db.rollback()
        raise
    response = JSONResponse(
        content=Token(access_token=access_token, token_type="bearer").model_dump()
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=False,  # True in production (HTTPS)
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        path="/auth",
    )
    return response


def logout(request: Request, db: Session):
    response = JSONResponse(content={"detail": "logged out"})
    response.delete_cookie("refresh_token", path="/auth")

    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        return response

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        sub = payload.get("sub")
        if jti and sub:
            rt = db.query(RefreshToken).filter_by(jti=jti, user_id=UUID(sub)).one_or_none()
            if rt and not rt.revoked_at:
                try:
                    rt.revoked_at = datetime.now(UTC)
                    db.commit()
                except Exception as e:
                    logging.error(
                        f"Failed to logout user {UUID(sub)}, "
                        f"error with Refresh Token change, error: {str(e)}"
                    )
                    db.rollback()
                    raise

    except InvalidTokenError:
        pass

    return response
