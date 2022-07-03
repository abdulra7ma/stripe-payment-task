# Python imports
import re

# Django imports
from django.conf import settings

# external imports
import jwt

# app imports
from lib.exceptions.core import ObjectNotFound


def get_token_user_id(token):
    """Get the user id for the decoded token"""

    payload = jwt.decode(
        jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"]
    )
    return payload["user_id"]


def get_jwt_token(request):
    """
    Get JWT token from the given request headers.

    Return:
        (token) -> if there is a token in request headers
    """

    headers = request.headers

    if "token" in request.query_params:
        return request.query_params["token"]

    if "token" in request.headers:
        return headers["token"]

    if "Authorization" in headers:
        if "Bearer" in headers["Authorization"]:
            return headers.get("Authorization")[7:]

    raise ObjectNotFound("Token not found")
