import json
import uuid
from pathlib import Path

from sqlalchemy.exc import IntegrityError

from src.database.core import Session_local
from src.entities.product import Product
from src.entities.order import Order


def get_items_from_json(file_name: str):
    file = Path(file_name)
    with Path.open(file, encoding="utf-8") as f:
        data = json.load(f)["products"]
    return data

def generate_sku(item: Product) -> str:
    """
    sku: <NAM>-<COL>-<SPA>-<RANDOM8>
    """
    prefix = "-".join([item.name[:3].lower(), item.collection[:3].lower(), item.space[:3].lower()])
    suffix = uuid.uuid4().hex[:8].upper()
    return f"{prefix}-{suffix}"[:64]


def add_to_db(products: {}, db, retry = 5):
    for item in products:
        new_product = Product(**item)
        new_product.is_active = True
        for attempt_num in range(retry):
            try:
                new_sku = generate_sku(new_product)
                new_product.sku = new_sku
                db.add(new_product)
                db.commit()
                db.refresh(new_product)
                break
            except IntegrityError as e:
                db.rollback()
                if "unique" in str(e).lower() or "uq" in str(e).lower():
                    continue
                raise


def delete_all_products(db):
    products = db.query(Product).all()
    for product in products:
        db.delete(product)
    db.commit()

def delete_all_orders(db):
    orders = db.query(Order).all()
    for order in orders:
        db.delete(order)
    db.commit()


with Session_local() as db:
    # items = get_items_from_json("products.json")
    # delete_all_products(db)
    delete_all_orders(db)
    # add_to_db(items, db)
