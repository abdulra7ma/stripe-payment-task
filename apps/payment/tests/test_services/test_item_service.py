import pytest
from django.db.utils import IntegrityError

from apps.payment.models import Item
from apps.payment.services.item import ItemService


@pytest.mark.django_db
def test_item_service_create_item():
    assert Item.objects.count() == 0

    service = ItemService()
    item = service.create_item(
        name="created_item", description="created_item description", price=12.5
    )

    assert Item.objects.count() == 1
    assert Item.objects.last().id == item.id


@pytest.mark.django_db
def test_item_service_create_item_with_None_values():
    assert Item.objects.count() == 0

    service = ItemService()

    with pytest.raises(IntegrityError) as e:
        item = service.create_item(name=None, description=None, price=None)

    assert Item.objects.count() == 0
