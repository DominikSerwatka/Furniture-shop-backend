from uuid import uuid4, UUID

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.auth.model import TokenData
from src.auth.service import get_password_hash
from src.database.core import Base
from src.entities.user import User


@pytest.fixture(scope="function")
def db_session():
    # use sqlLite database for testing
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def create_test_user():
    def return_user(
        email: str = "test@gmail.com",
        password: str = "test_password",
        name: str = "test_name",
        last_name: str = "test_last_name",
    ):
        test_user = User(
            id=uuid4(),
            email=email,
            name=name,
            last_name=last_name,
            password_hash=get_password_hash(password),
        )
        return test_user

    return return_user


@pytest.fixture()
def test_token_data():
    def return_token_data(uuid: UUID):
        return TokenData(user_id=str(uuid))

    return return_token_data
