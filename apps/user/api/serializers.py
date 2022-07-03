# Django imports
from django.conf import settings
from django.contrib.sites.models import Site
import os

# external imports
from base.serializers.helpers import serializer_error_messages
from user.models import User, UserPic
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator

# app imports
from apps.base.serializers.core import CoreModelSerializer


class UserSerializer(CoreModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "middle_name",
            "surname",
            "email",
            "phone_number",
            "birthday",
            "city",
        )
        extra_kwargs = {
            "first_name": {
                "required": False,
                "error_messages": {
                    **serializer_error_messages("first_name", max_length=True)
                },
            },
            "middle_name": {
                "required": False,
                "error_messages": {
                    **serializer_error_messages("middle_name", max_length=True)
                },
            },
            "surname": {
                "required": False,
                "error_messages": {
                    **serializer_error_messages("surname", max_length=True)
                },
            },
            "city": {
                "error_messages": {
                    **serializer_error_messages("city", max_length=True)
                }
            },
        }


class UserUpdateModelSerializer(CoreModelSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            "first_name",
            "middle_name",
            "surname",
            "phone_number",
            "birthday",
            "city",
            "email",
        )
        read_only_fields = ["email"]


class UserPicResponceSerializer(CoreModelSerializer):
    picture = serializers.SerializerMethodField()
    thumb_picture = serializers.SerializerMethodField()

    class Meta:
        model = UserPic
        fields = ["picture", "thumb_picture"]

    def get_picture(self, obj):
        if not os.path.exists(obj.picture.path):
            return ""

        return "http://%s%s%s" % (
            Site.objects.get_current().domain,
            settings.MEDIA_URL,
            obj.picture,
        )

    def get_thumb_picture(self, obj):
        if not os.path.exists(obj.thumb_picture.path):
            return ""

        return "http://%s%s%s" % (
            Site.objects.get_current().domain,
            settings.MEDIA_URL,
            obj.thumb_picture,
        )


class UserPicSerializer(CoreModelSerializer):
    class Meta:
        model = UserPic
        fields = ["user", "picture"]
        # exclude = ["thumb_picture"]
        extra_kwargs = {
            "picture": {"write_only": True},
        }

    def validate_picture(self, picture):
        MAX_FILE_SIZE = 5242880
        ALLOWED_FILE_FORMATS = ["jpeg", "jpg", "png", "svg", "gif", "tiff"]

        if picture.name.split(".")[-1].lower() not in ALLOWED_FILE_FORMATS:
            raise serializers.ValidationError(
                detail="Image file format not supported please user another format.",
                code=status.HTTP_400_BAD_REQUEST,
            )

        if picture.size > MAX_FILE_SIZE:
            raise serializers.ValidationError(
                detail="Please keep filesize under five megabytes.",
                code=status.HTTP_400_BAD_REQUEST,
            )

        return picture

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # data["thumb_picture"] = self.instance.thumb_picture.path
        data["pics"] = UserPicResponceSerializer(instance=instance).data
        return data
