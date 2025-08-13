from sqlalchemy.orm import Session

import logging
from src.entities.product import Product
from src.products.model import ProductResponse


def get_all_products(db: Session) -> list[ProductResponse]:
    products = db.query(Product).all()
    logging.info(f"Retrieved {len(products)} of products.")
    return products
