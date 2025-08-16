from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from src.api import register_routes
from src.logging import configure_logging, LogLevels

configure_logging(LogLevels.info)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'], # my react front-end
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

"""Only uncomment below to create new tables"""
# Base.metadata.create_all(bind=engine)

register_routes(app)