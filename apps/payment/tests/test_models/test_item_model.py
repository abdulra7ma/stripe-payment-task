import pytest
from django.db.utils import IntegrityError

from apps.payment.models import Item

data = {"name": "item-1", "description": "item-1 description", "price": 13.50}


@pytest.mark.django_db
def test_item_object_creation():
    assert Item.objects.count() == 0

    # create new item object
    item = Item(**data)

    # ensure that the object has not been saved yet
    assert Item.objects.count() == 0

    # save item to db
    item.save()

    assert Item.objects.count() == 1
    assert item.name == data["name"]
    assert item.description == data["description"]
    assert item.price == data["price"]


@pytest.mark.django_db(transaction=True)
def test_item_object_creation_failure():
    assert Item.objects.count() == 0

    # delete price from data dict
    del data["price"]

    # create new item object
    item = Item(**data)

    # ensure that the object has not been saved yet
    assert Item.objects.count() == 0

    # assert IntegrityError error as the price field not included
    # in the data dict
    with pytest.raises(IntegrityError) as exc_info:
        # save item to db
        item.save()

    # ensure that the object has not been saved yet
    assert Item.objects.count() == 0
