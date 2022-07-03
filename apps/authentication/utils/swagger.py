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
                        "phone_number": "000-0000-0000",
                        "birthday": "2004-04-24",
                        "city": "New York",
                    },
                    "flights": [
                        {
                            "id": 1,
                            "departure_airport": "Shag",
                            "arrival_airport": "Hang",
                            "flight_number": "HGFSAB765JJJK",
                            "departure_time": "21:57:32",
                            "departure_date": "2022-02-18",
                            "arrive_time": "21:57:34",
                            "arrive_date": "2022-02-18",
                            "user": 1,
                        },
                        {
                            "id": 2,
                            "departure_airport": "Wang",
                            "arrival_airport": "Sang",
                            "flight_number": "flds;fmlkdskflds",
                            "departure_time": "21:57:32",
                            "departure_date": "2022-02-18",
                            "arrive_time": "21:57:34",
                            "arrive_date": "2022-02-18",
                            "user": 1,
                        },
                    ],
                    "passengers": [
                        {
                            "id": 1,
                            "date_joined": "2022-01-29T03:01:14.959419",
                            "updated": "2022-01-29T03:01:14.959432",
                            "first_name": "Jack",
                            "surname": "Mac",
                            "passenger_type": "AD",
                            "email": "jack_@hotmail.com",
                            "gender": "M",
                            "date_of_birth": "2002-09-18",
                            "passport_id": "A334ijfdgdfl3",
                            "passport_date_of_issue": "2018-09-28",
                            "passport_date_of_expiry": "2028-09-29",
                            "country": "",
                            "user": 42,
                            "address": "null",
                        },
                    ],
                    "profile_picture": {
                        "picture": ".../picture.png",
                        "thumb_picture": ".../picture_thumb.png",
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
