# Python imports
import json

# Django imports
from django.conf import settings

# external imports
import jwt
from rest_framework import serializers

# app imports
from lib.exceptions.core import InvaildToken


def serializer_validate_token(token) -> str:
    try:
        jwt.decode(
            jwt=token,
            key=settings.SECRET_KEY,
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError as e:
        raise serializers.ValidationError("Link expired", code="token_expired")
    except jwt.exceptions.DecodeError as e:
        raise serializers.ValidationError("Invalid link", code="invaild_token")

    return token


def validate_token(token) -> dict:
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.SECRET_KEY,
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError as e:
        raise InvaildToken("Token expired", code="token_expired")
    except jwt.exceptions.DecodeError as e:
        raise InvaildToken("Invalid token", code="invaild_token")
    return payload


def verify_email_token(token):
    try:
        jwt.decode(
            jwt=token,
            key=settings.SECRET_KEY,
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError as e:
        raise InvaildToken("Link expired", code="link_expired")
    except jwt.exceptions.DecodeError as e:
        raise InvaildToken("Invalid link", code="invaild_link")

    return token
