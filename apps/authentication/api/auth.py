# Django imports
from django.core import exceptions

# external imports
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

# app imports
from .exceptions import AlreadyLoggedIn


class AlreadyLoggedIn(BaseAuthentication):
    def authenticate(self, request):
        try:
            """
            Checks the user login status

            Returns:
                if the user is logged in, func will raise an exception
                that returns a 406 http respone
            """
            # if request.user.is_authenticated:

            #     # get `message` argument from `kwargs` and pass it
            #     # as a value to the `msg` key else the default
            #     # value is going to be used
            raise AuthenticationFailed("Already  logged in")

        except RecursionError:
            pass
