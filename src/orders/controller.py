import logging
from uuid import UUID

from fastapi import APIRouter
from starlette import status

from src.auth.service import CurrentUser
from src.database.core import DbSession
from src.orders.model import OrderCreate, OrderResponse
from src.orders.service import create_order, get_orders, get_order_by_id

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order_controller(db: DbSession, order: OrderCreate, current_user: CurrentUser):
    return create_order(current_user, db, order)

@router.get("/", response_model=list[OrderResponse])
def get_orders_controller(db: DbSession, current_user: CurrentUser):
    return get_orders(current_user, db)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order_controller(db: DbSession, current_user: CurrentUser, order_id: UUID):
    return get_order_by_id(current_user, db, order_id)
