import pytest

from apps.payment.models import Item
from apps.payment.selectors.item import get_item_by_id


@pytest.mark.django_db
def test_get_item_by_id_with_exist_item_id():
    assert Item.objects.count() == 0

    # create new item object
    item = Item.objects.create(
        name="item-1", description="item-1 description", price=33.5
    )

    # ensure object creation
    assert Item.objects.count() == 1

    result = get_item_by_id(item.id)

    assert result is not None
    assert result.id == item.id


@pytest.mark.django_db
def test_get_item_by_id_with_non_exist_item_id():
    assert Item.objects.count() == 0

    result = get_item_by_id(1)

    assert result is None
