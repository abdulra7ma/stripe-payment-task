from apps.payment.models import Item, Order

def create_order(item: Item):
    """
    Create new Order object


    :param Item item: item to be created
    """