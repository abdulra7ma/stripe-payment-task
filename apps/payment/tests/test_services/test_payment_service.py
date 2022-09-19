import json

import pytest
from django.http.response import JsonResponse

from apps.payment.models import Item
from apps.payment.services.payment import PaymentService


@pytest.mark.django_db
def test_create_checkout_session_with_valid_item_object():
    assert Item.objects.count() == 0

    # create new item object
    item = Item.objects.create(
        name="item-1", description="item-1 description", price=33.5
    )

    # ensure object creation
    assert Item.objects.count() == 1

    result = PaymentService().create_checkout_session(item)

    assert result is not None
    assert isinstance(result, JsonResponse)
    assert "sessionId" in json.loads(result.content)


@pytest.mark.django_db
def test_create_checkout_session_with_invalid_item_object():
    result = PaymentService().create_checkout_session("dsjfsd")

    assert isinstance(result, JsonResponse)
    assert "error" in json.loads(result.content)
