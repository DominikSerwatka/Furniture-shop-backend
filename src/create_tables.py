from src.database.core import Base, engine

from src.entities.user import User
from src.entities.address import Address

Base.metadata.create_all(bind=engine)