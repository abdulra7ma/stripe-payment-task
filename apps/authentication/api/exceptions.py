# external imports
from rest_framework.exceptions import APIException


class AlreadyLoggedIn(APIException):
    """
    Raised when a user attepmts to logging while logged in
    """
    
    status_code = 406
    default_detail = "Your's already logged in"
    default_code = "already_logged_in"


class CustomErrorException(APIException):
    status_code = 404
    default_detail = "Custom error"
    default_code = "custom_error"

    def __init__(self, detail=None, code=None, status_code=None):
        super().__init__(detail, code)
        self.default_detail = (
            detail if detail is not None else self.default_detail
        )
        self.status_code = (
            status_code if status_code is not None else self.status_code
        )
        self.default_code = code if code is not None else self.default_code
