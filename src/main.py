from fastapi import FastAPI

from src.api import register_routes
from src.database.core import Base, engine
from src.logging import configure_logging, LogLevels

configure_logging(LogLevels.info)

app = FastAPI()

"""Only uncomment below to create new tables"""
# Base.metadata.create_all(bind=engine)

register_routes(app)