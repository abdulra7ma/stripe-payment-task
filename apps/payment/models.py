from django.db import models
from django.utils import timezone


class DateTimeMixin(models.Model):
    """Abstract Date Time model"""

    date_joined = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Item(DateTimeMixin):
    name = models.CharField(verbose_name="Item Name", max_length=256)
    description = models.TextField(verbose_name="Item Description")
    price = models.DecimalField(
        verbose_name="Item Price", max_digits=12, decimal_places=2
    )
