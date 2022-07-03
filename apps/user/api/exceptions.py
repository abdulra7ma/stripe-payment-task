# external imports
from rest_framework.exceptions import APIException


class CustomerNotFound(APIException):
    """Raise a HTTP 404 error when Customer not found in the DB"""

    status_code = 404
    default_detail = "There is no such a customer with this ID in our DB"
    default_code = "customer_not_found"


class NotCorrectParameters(APIException):
    """Raise a HTTP 400 error, if query params not Correct or not provided"""

    status_code = 400
    default_detail = "Not correct query parameters"
    default_code = "not_correct_query_params"


