# external imports
from rest_framework import serializers

# app imports
from .mixins import RequiredMessageSerializerMixin


class CoreSerializer(RequiredMessageSerializerMixin, serializers.Serializer):
    """
    DRF default serializer that overwrites the default error messages
    """


class CoreModelSerializer(
    RequiredMessageSerializerMixin, serializers.ModelSerializer
):
    """
    DRF model serializer that overwrites the default error messages
    """
