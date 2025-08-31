from fastapi import APIRouter
from starlette import status

from src.auth.service import CurrentUser
from src.database.core import DbSession
from src.orders.model import OrderCreate, OrderResponse
from src.orders.service import create_order

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order_controller(db: DbSession, order: OrderCreate, current_user: CurrentUser):
    return create_order(current_user, db, order)
