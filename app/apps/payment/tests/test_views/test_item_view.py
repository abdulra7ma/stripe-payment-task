import pytest
from django.urls import reverse

from apps.payment.models import Item


@pytest.mark.django_db
def test_get_item_view_page_success(client):
    # create new item object
    item = Item.objects.create(
        name="item-1", description="item-1 description", price=33.5
    )
    url = reverse("item", kwargs={"item_id": item.id})

    response = client.get(url)

    assert response.status_code == 200
    assert str(item.name) in response.content.decode("utf-8")
    assert str(item.price) in response.content.decode("utf-8")
    assert str(item.description) in response.content.decode("utf-8")


@pytest.mark.django_db
def test_get_item_view_page_failure(client):
    url = reverse("item", kwargs={"item_id": 2})
    response = client.get(url)

    assert response.status_code == 404
    assert (
        "The requested resource was not found on this server."
        in response.content.decode("UTF-8")
    )
