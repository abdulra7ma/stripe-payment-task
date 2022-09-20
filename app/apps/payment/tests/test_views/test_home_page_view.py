import pytest
from django.urls import reverse

from apps.payment.models import Item


@pytest.mark.django_db
def test_home_page_view_with_valid_get_method(client):
    url = reverse("home-page")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_home_page_view_with_invalid_method(client):
    url = reverse("home-page")
    response = client.post(url)
    assert response.status_code == 405


@pytest.mark.django_db
def test_home_page_view_with_item_object_included_in_ui(client):
    url = reverse("home-page")

    # create new item object
    item = Item.objects.create(
        name="item-1", description="item-1 description", price=33.5
    )

    response = client.get(url)

    assert response.status_code == 200
    assert str(item.name) in response.content.decode("utf-8")
    assert str(item.price) in response.content.decode("utf-8")
    assert str(item.description) in response.content.decode("utf-8")
