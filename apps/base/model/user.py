# Django imports
# Django imports
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

# external imports
from user.managers import CustomUserManager
from user.utils.constants import ModelConst


class CustomUser(PermissionsMixin, AbstractBaseUser):
    """
    Abstract User model that defines comman attributes
    that can inhertited by other models. This model uses email
    inside of username for login and other authentication layers.
    """

    email = models.EmailField(ModelConst.EMAIL, unique=True)
    is_active = models.BooleanField(ModelConst.IS_ACTIVE, default=False)
    is_frozen = models.BooleanField(ModelConst.IS_FROZEN, default=False)
    is_staff = models.BooleanField(ModelConst.IS_STAFF, default=False)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    class Meta:
        abstract = True
