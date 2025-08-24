import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

load_dotenv()

"""You can add a DATABASE_URL to environment variable to your .env file"""
DATABASE_URL = os.getenv("DATABASE_URL")

"""Or you can hard code SQLite here"""

# DATABASE_URL = "sqlite:///./shopapp.db"

"""Or you can hard code PostgresSQL here"""
# DATABASE_URL = "postgresql://postgres:postgres@db:5432/shopapp"

engine = create_engine(DATABASE_URL)

Session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]
