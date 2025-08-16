from typing import List
from uuid import UUID

from fastapi import APIRouter

from src.database.core import DbSession
from src.products.model import ProductResponse
from src.products.service import get_all_products, get_product_by_id

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/all", response_model=List[ProductResponse])
def get_all_products_controller(db: DbSession):
    return get_all_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_controller(db: DbSession, product_id: UUID):
    return get_product_by_id(db, product_id)