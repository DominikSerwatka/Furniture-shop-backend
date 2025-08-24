from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import register_routes
from src.logging import LogLevels, configure_logging

configure_logging(LogLevels.info)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # my react front-end
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""Only uncomment below to create new tables"""
# Base.metadata.create_all(bind=engine)

register_routes(app)
