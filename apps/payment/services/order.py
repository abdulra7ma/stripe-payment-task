from django.db import transaction

from apps.payment.models import Item, Order


class OrderService:
    @transaction.atomic
    def create_order(self, *, item: Item = None):
        """
        Create new Order object

        :param Item item: item to be created

        :return: newly created Order object
        :rtype: Order

        """

        order = Order(item=item)
        order.save()

        return order
