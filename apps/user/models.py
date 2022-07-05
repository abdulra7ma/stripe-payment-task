# Django imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# external imports
from user.utils.image import compress

# app imports
from apps.base.model.user import CustomUser
from lib.constants.const import Const

# app imports
from .mixins import DateTimeMixin
from .utils.constants import ModelConst


class User(DateTimeMixin, CustomUser):
    """
    User model defines basic user attributes for login and signup
    """

    first_name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH, help_text=ModelConst.FIRST_NAME
    )
    middle_name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH, help_text=ModelConst.MIDDLE_NAME
    )
    surname = models.CharField(
        max_length=Const.NAME_MAX_LENGTH, help_text=ModelConst.SURNAME
    )

    phone_number = models.CharField(
        max_length=Const.PHONE_NUMBER_MAX_LENGTH, blank=True
    )
    birthday = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=ModelConst.CITY_MAX_LENGHT, blank=True)

    REQUIRED_FIELDS = ["first_name", "surname"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        app_label = "user"

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return self.first_name + " " + self.surname


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "users_pics/user_{0}/{1}".format(instance.user.id, filename)


class UserPic(DateTimeMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.FileField(upload_to=user_directory_path, blank=True, null=True, default="default_pro_pic.jpeg")
    thumb_picture = models.ImageField(blank=True)

    # calling image compression function before saving the data
    def save(self, *args, **kwargs):
        new_image = compress(self.picture)
        self.picture = new_image
        super().save(*args, **kwargs)

