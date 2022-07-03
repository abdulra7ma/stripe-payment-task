# Python imports
import os

# Django imports
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

# external imports
from user.utils.image import thumbnail_image

# app imports
from .models import UserPic


@receiver(models.signals.post_delete, sender=UserPic)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes related user image from filesystem
    when corresponding `UserPic` object is deleted.
    """

    if instance.picture:
        if os.path.isfile(instance.picture.path):
            os.remove(instance.picture.path)

    if instance.thumb_picture:
        if os.path.isfile(instance.thumb_picture.path):
            os.remove(instance.thumb_picture.path)


@receiver(models.signals.pre_save, sender=UserPic)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `UserPic` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_user_pic = UserPic.objects.get(pk=instance.pk).picture
    except UserPic.DoesNotExist:
        return False

    new_user_picture = instance.picture
    if not old_user_pic == new_user_picture:
        if os.path.isfile(old_user_pic.path):
            os.remove(old_user_pic.path)

    try:
        old_user_thumb_pic = UserPic.objects.get(pk=instance.pk).picture
    except UserPic.DoesNotExist:
        return False

    new_user_thumb_pic = instance.picture
    if not old_user_thumb_pic == new_user_thumb_pic:
        if os.path.isfile(old_user_thumb_pic.path):
            os.remove(old_user_thumb_pic.path)


@receiver(post_save, sender=UserPic)
def add_thumbnil_file_to_user_pic_object(sender, instance, **kwargs):
    if not instance.thumb_picture:
        thumb_picture_url = thumbnail_image(instance.picture)
        instance.thumb_picture = thumb_picture_url
        instance.save()
