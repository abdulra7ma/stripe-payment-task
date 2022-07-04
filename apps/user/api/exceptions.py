# external imports
from rest_framework.exceptions import APIException


class userNotFound(APIException):
    """Raise a HTTP 404 error when User not found in the DB"""

    status_code = 404
    default_detail = "User does not exists"
    default_code = "user_not_found"


class NotCorrectParameters(APIException):
    """Raise a HTTP 400 error, if query params not Correct or not provided"""

    status_code = 400
    default_detail = "Not correct query parameters"
    default_code = "not_correct_query_params"
