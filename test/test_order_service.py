from decimal import Decimal

from src.entities.address import Address
from src.entities.product import Product
from src.orders.model import AddressSnapshot, OrderCreate, OrderItemCreate
from src.orders.service import create_order


def test_create_order(test_token_data, db_session, create_test_user):
    new_user = create_test_user()
    db_session.add(new_user)

    db_session.commit()

    new_token_data = test_token_data(new_user.id)

    new_delivery_address = Address(
        user_id=new_user.id,
        name="Name",
        last_name="LastName",
        email=new_user.email,
        phone_number="111222333",
        street="Ulica",
        house_number="1",
        postal_code="1",
        city="City",
    )
    db_session.add(new_delivery_address)
    db_session.commit()
    new_product = Product(
        name="Szafa",
        price=100,
        description="Przestronna szafa przesuwna",
        sku="szafa-1",
        picture="url_to_picture",
        space="sypialnia",
        material="drewno",
        collection="lato-2025",
        is_active=True,
    )
    db_session.add(new_product)
    db_session.commit()

    order_item_create = OrderItemCreate(
        product_id=new_product.id,
        qty=1,
    )
    new_delivery_address_snapshot = AddressSnapshot(
        name=new_delivery_address.name,
        last_name=new_delivery_address.last_name,
        email=new_delivery_address.email,
        phone_number=new_delivery_address.phone_number,
        street=new_delivery_address.street,
        house_number=new_delivery_address.house_number,
        postal_code=new_delivery_address.postal_code,
        city=new_delivery_address.city,
    )
    order_to_create = OrderCreate(
        items=[order_item_create],
        delivery_address_snapshot=new_delivery_address_snapshot,
        delivery_address_id=new_delivery_address.id,
        delivery_fee=Decimal(10),
        discount_total=Decimal(10),
        payment_method="Blik",
    )
    order = create_order(new_token_data, db_session, order_to_create)
    assert order
