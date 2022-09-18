from apps.payment.models import Item


def get_item_by_id(item_id: int) -> Item | None:
    """
    Get Item object by Item id

    :param int item_id: reference id of Item

    :return: the Item object
    :rtype: Item

    """
    try:
        return Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return None