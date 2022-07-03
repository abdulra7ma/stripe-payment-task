# Django imports
from django.db import models
from django.utils import timezone


class DateTimeMixin(models.Model):
    """Abstract Date Time model"""

    date_joined = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
