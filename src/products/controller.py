from typing import List

from fastapi import APIRouter

from src.database.core import DbSession
from src.products.model import ProductResponse
from src.products.service import get_all_products

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/all", response_model=List[ProductResponse])
def get_all_products_controller(db: DbSession):
    return get_all_products(db)
