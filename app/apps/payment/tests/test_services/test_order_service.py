import pytest
from django.db.utils import IntegrityError

from apps.payment.models import Item, Order
from apps.payment.services.order import OrderService


@pytest.mark.django_db
def test_order_service_create_item(item):
    assert Item.objects.count() == 1
    assert Order.objects.count() == 0

    service = OrderService()
    order = service.create_order(item=item)

    assert Order.objects.count() == 1
    assert order.item.id == item.id


@pytest.mark.django_db
def test_order_service_create_item_with_None_values():
    assert Item.objects.count() == 0
    assert Order.objects.count() == 0

    service = OrderService()

    with pytest.raises(IntegrityError) as e:
        order = service.create_order(item=None)

    assert Order.objects.count() == 0
