import pytest

from apps.payment.models import Order
from apps.payment.services.order import OrderService


@pytest.mark.django_db
def test_order_object_creation(item):
    assert Order.objects.count() == 0

    order = OrderService().create_order(item=item)

    assert Order.objects.count() == 1

    assert order.item.id == item.id
