import logging
from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.auth.model import TokenData
from src.entities.address import Address
from src.entities.order import Order, OrderItem, OrderStatus
from src.entities.product import Product
from src.exceptions import OrderNotFoundException
from src.orders.model import OrderCreate, OrderResponse


def _check_address_belongs_to_user(db: Session, address_id: UUID, user_id: UUID):
    address = db.query(Address).filter(Address.id == address_id).one_or_none()
    if address.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Address not accessible")


def _money(price) -> Decimal:
    return (Decimal(price)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def create_order(current_user: TokenData, db: Session, order: OrderCreate) -> Order:
    if not order.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order must have items")

    user_id = current_user.get_uuid()

    if order.delivery_address_id:
        _check_address_belongs_to_user(db, order.delivery_address_id, user_id)

    all_products = db.query(Product).all()
    products_map = {product.id: product for product in all_products}
    all_product_ids = {product.id for product in all_products}

    order_product_ids = {order_item.product_id for order_item in order.items}
    matched = all_product_ids & order_product_ids
    if matched != order_product_ids:
        missing = order_product_ids - matched
        msg = f"Products not found: {missing}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

    order_item_list_to_create: list[OrderItem] = []
    for item in order.items:
        product = products_map[item.product_id]
        if not product.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product {product.id} is inactive")
        unit_price = _money(product.price)
        qty = int(item.qty)
        line_total = _money(unit_price * qty)
        new_order_item = OrderItem(
            product_id=product.id,
            sku_snapshot=product.sku,
            name_snapshot=product.name,
            image_url_snapshot=product.picture,
            unit_price_snapshot=unit_price,
            qty=qty,
            line_total=line_total,
        )
        order_item_list_to_create.append(new_order_item)

    items_total = _money(sum(item.line_total for item in order_item_list_to_create))
    delivery_fee = _money(order.delivery_fee)
    discount_total = _money(order.discount_total)
    grand_total = _money(items_total + delivery_fee - discount_total)

    if grand_total < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Grand total cannot be negative")

    new_order = Order(
        user_id=user_id,
        delivery_address_snapshot=order.delivery_address_snapshot.model_dump(),
        delivery_address_id=order.delivery_address_id,
        items_total=items_total,
        delivery_fee=delivery_fee,
        discount_total=discount_total,
        grand_total=grand_total,
        status=OrderStatus.PLACED,
        payment_method=order.payment_method,
    )
    new_order.items = order_item_list_to_create

    try:
        db.add(new_order)
        db.flush()
        db.commit()
        db.refresh(new_order)
        return new_order
    except Exception as e:
        logging.warning(f"Failed to create order: {str(e)}")
        db.rollback()
        raise


def get_orders(current_user: TokenData, db: Session) -> list[OrderResponse]:
    user_id = current_user.get_uuid()
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders


def get_order_by_id(current_user: TokenData, db: Session, order_id: UUID) -> OrderResponse:
    order = db.query(Order).filter(Order.id == order_id).filter(Order.user_id == current_user.get_uuid()).one_or_none()
    if not order:
        logging.warning(f"Order {order_id} not found for user {current_user.get_uuid()}")
        raise OrderNotFoundException(order_id)
    logging.info(f"Retrieved order {order_id} for user {current_user.get_uuid()}")
    return order
