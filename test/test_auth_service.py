from datetime import timedelta, datetime, timezone
import json
import os

import jwt


from src.auth.service import get_password_hash, verify_password, authenticate_user, login_for_access_token
from src.entities.refresh_token import RefreshToken


class FormData:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.scope = ""
        self.client_id = None
        self.client_secret = None


def test_verify_password():
    password = "password1234"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password)
    assert not verify_password("wrong_password", hashed_password)

def test_authenticate_user(db_session, create_test_user):
    password = "password123"
    email = "test@gmail.com"
    test_user = create_test_user(email, password)
    db_session.add(test_user)
    db_session.commit()

    user = authenticate_user(email, password, db_session)
    assert user is not False
    assert user.email == "test@gmail.com"


def test_login_for_access_token(db_session, create_test_user):
    password = "password123"
    email = "test@gmail.com"
    test_user = create_test_user(email, password)
    db_session.add(test_user)
    db_session.commit()

    form_data = FormData(username=email, password=password)
    result = login_for_access_token(form_data, db_session)
    assert result.status_code == 200

    data = json.loads(result.body.decode("utf-8"))
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    set_cookie = result.headers.get("set-cookie")
    assert set_cookie is not None
    assert "refresh_token=" in set_cookie
    assert "HttpOnly" in set_cookie
    assert "Path=/auth" in set_cookie
    assert "SameSite=lax" in set_cookie

    cookie_value = set_cookie.split("refresh_token=", 1)[1].split(";", 1)[0]
    parts = cookie_value.split(".")
    assert len(parts) == 3  # JWT powinien mieć 3 segmenty

    payload = jwt.decode(cookie_value, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
    assert "sub" in payload and "jti" in payload and "exp" in payload
    assert payload["sub"] == str(test_user.id)

    rt = db_session.query(RefreshToken).filter_by(user_id=test_user.id, jti=payload["jti"]).one_or_none()
    assert rt is not None
    assert rt.revoked_at is None
    assert rt.expires_at.timestamp() > datetime.now(timezone.utc).timestamp()
