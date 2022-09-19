import pytest

from apps.payment.services.item import ItemService


@pytest.fixture
def item():
    return ItemService().create_item(
        name="item-one", description="description of the item", price=25.6
    )
