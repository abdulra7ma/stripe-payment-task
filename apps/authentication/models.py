# Django imports
from django.db import models
from django.utils import timezone

# external imports
from user.models import User

# app imports
from lib.constants.const import Const


class LoginDeviceManager(models.Manager):
    pass


class LoginDevice(models.Model):
    user = models.ForeignKey(
        User,
        related_name="device_user",
        on_delete=models.CASCADE,
        null=True,
    )
    device = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    os = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    browser = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    ip_address = models.CharField(
        max_length=Const.IP_ADDRESS_MAX_LENGTH,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    is_registered = models.BooleanField(default=False)

    objects = LoginDeviceManager()

    class Meta:
        ordering = ("-id",)
        app_label = "authentication"
