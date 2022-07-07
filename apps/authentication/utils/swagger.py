# external imports
from drf_yasg import openapi

login_response_schema_dict = {
    "406": openapi.Response(
        description="Error response",
        examples={
            "application/json": {
                "message": "Invalid email address.",
                "status": {"code": 401, "message": "null"},
                "body": {},
                "fail": True,
            }
        },
    ),
    "201": openapi.Response(
        description="Success response",
        examples={
            "application/json": {
                "message": "Successfully signed In",
                "status": {
                    "code": 200,
                    "message": "Successfully signed In",
                },
                "body": {
                    "tokens": {
                        "access": "user-access-token",
                        "refresh": "user-refresh-token",
                    },
                    "success": True,
                    "user": {
                        "id": 1,
                        "first_name": "first-name",
                        "middle_name": "middle_name",
                        "surname": "surname",
                        "email": "user@user.com",
                    },
                    "success": True,
                },
            },
        },
    ),
}

# AirportSearchView parameters
token_param = openapi.Parameter(
    "token",
    in_=openapi.IN_QUERY,
    description="Email change token",
    type=openapi.TYPE_STRING,
    required=True,
)

email_address_param = openapi.Parameter(
    "email_address",
    in_=openapi.IN_QUERY,
    description="Enter email address to get password reset email",
    type=openapi.TYPE_STRING,
    required=True,
)
