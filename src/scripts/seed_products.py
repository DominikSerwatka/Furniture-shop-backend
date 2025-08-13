import json
from pathlib import Path

from src.database.core import Session_local
from src.entities.product import Product


def get_items_from_json(file_name: str):
    file = Path(file_name)
    with open(file, encoding="utf-8") as f:
        data = json.load(f)["products"]
    return data

def add_to_db(products: {}, db):
    for item in products:
        new_product = Product(**item)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)


with Session_local() as db:
    items = get_items_from_json("products.json")
    add_to_db(items, db)