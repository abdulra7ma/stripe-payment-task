# external imports
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response


class AlreadyLoggedInMixin:
    def dispatch(self, request, *args, **kwargs):
        """
        Checks the user login status

        Return:
            if the user is logged in return a 406 http respone

        """

        if request.user.is_authenticated:
            # get `message` argument from `kwargs` and pass it
            # as a value to the `msg` key else the default
            # value is going to be used
            msg = {
                "message": kwargs.get(
                    "message",
                    None,
                )
                or "Already logged in"
            }

            # initalize a `HTTPRequest` instance from the default DRF
            # HTTPRequest object by passing the coming args and kwargs
            # to the initialize_request func
            request = self.initialize_request(request, *args, **kwargs)

            # assgin the new request instance to the internal
            # request object
            self.request = request
            self.headers = self.default_response_headers
            response = Response(
                data=msg, status=status.HTTP_406_NOT_ACCEPTABLE
            )

            # finalize response internal method takes mainly two parameters
            # request and response and returns a complete response object to be
            # send to the client
            self.response = self.finalize_response(
                request, response, *args, **kwargs
            )

            return self.response

        return super().dispatch(request, *args, **kwargs)
