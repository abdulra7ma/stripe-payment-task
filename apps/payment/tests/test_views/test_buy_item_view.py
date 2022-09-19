import json

import pytest
from django.urls import reverse

from apps.payment.models import Item


@pytest.mark.django_db
def test_get_checkout_session_id_from_buy_item_view_success(client):
    # create new item object
    item = Item.objects.create(
        name="item-1", description="item-1 description", price=33.5
    )

    url = reverse("buy-item", kwargs={"item_id": item.id})

    response = client.get(url)

    assert response.status_code == 200
    assert "sessionId" in json.loads(response.content)


@pytest.mark.django_db
def test_get_checkout_session_id_with_non_exist_item_object(client):
    url = reverse("buy-item", kwargs={"item_id": 1})

    response = client.get(url)

    assert response.status_code == 404
    assert "Not Found" in response.content.decode("UTF-8")
