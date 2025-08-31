from fastapi import FastAPI

from src.addresses.controller import router as addresses_router
from src.auth.controller import router as auth_router
from src.products.controller import router as products_router
from src.users.controller import router as users_router
from src.orders.controller import router as order_router


def register_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(addresses_router)
    app.include_router(products_router)
