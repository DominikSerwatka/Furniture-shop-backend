from src.database.core import Base, engine

from src.entities.user import User
from src.entities.address import Address
from src.entities.refresh_token import RefreshToken
from src.entities.product import Product

Base.metadata.create_all(bind=engine)