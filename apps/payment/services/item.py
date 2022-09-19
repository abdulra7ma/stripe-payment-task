from django.db import transaction

from apps.payment.models import Item


class ItemService:
    @transaction.atomic
    def create_item(
        self, *, name: str = None, description: str = None, price: float = None
    ):
        """
        Create an item object

        :param str name: item name
        :param str description: item description
        :param flaot price: item price

        :return: Newly created Item object
        :rtype: Item

        """
        
        item = Item(name=name, description=description, price=price)
        item.save()
        return item
