from uuid import UUID

from sqlalchemy.orm import Session

import logging
from src.entities.product import Product
from src.exceptions import ProductNotFoundError
from src.products.model import ProductResponse


def get_all_products(db: Session) -> list[ProductResponse]:
    products = db.query(Product).all()
    logging.info(f"Retrieved {len(products)} of products.")
    return products


def get_product_by_id(db: Session, product_id: UUID) -> ProductResponse:
    product = db.query(Product).filter(Product.id == product_id).one_or_none()
    if not product:
        logging.warning(f"Product {product_id} not found")
        raise ProductNotFoundError(product_id)
    logging.info(f"Retrieved product {product_id}")
    return product
