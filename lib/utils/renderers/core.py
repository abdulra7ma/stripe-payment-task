# Python imports
from collections import namedtuple

# external imports
from rest_framework.exceptions import ErrorDetail
from rest_framework.renderers import JSONRenderer


class RootJSONRenderer(JSONRenderer):
    def render(
        self, response_body, accepted_media_type=None, renderer_context=None
    ):
        """
        Json renderer class for custom response for both succuss and fail responses
        """

        self.response = renderer_context["response"]

        # if the coming response object is not a custom response
        # object than add the `status_message` attribute
        if not hasattr(self.response, "status_message"):
            setattr(
                self.response,
                "status_message",
                None,
            )

            try:
                self.response.status_message = self.response.data[
                    "detail"
                ].code
            except Exception:
                pass

        if self.is_amadaus_response():
            amadous_status_message = response_body["errors"][0]["title"]
            self.response.status_message = amadous_status_message

        status_message = self.response.status_message

        status_code = self.response.status_code
        if str(status_code).startswith("2"):
            self.response = self.success_response(
                response_body, status_code, status_message
            )
        else:
            self.response = self.error_response(
                response_body, status_code, status_message
            )

        return super(RootJSONRenderer, self).render(
            self.response, accepted_media_type, renderer_context
        )

    def success_response(self, data, status_code, status_message=None):
        success_response = self.get_response_format

        success_response["message"] = status_message
        success_response["body"] = data
        success_response["success"] = True
        success_response["status"]["code"] = status_code
        success_response["status"]["message"] = status_message

        return success_response

    def error_response(self, data, status_code, status_message):
        error_response = self.get_response_format

        error_response["message"] = self.get_error_message(data)
        error_response["body"] = {}
        error_response["fail"] = True
        error_response["status"]["code"] = status_code
        error_response["status"]["message"] = status_message

        return error_response

    @property
    def get_response_format(self):
        return {
            "message": "",
            "status": {
                "code": "",
                "message": "",
            },
            "body": {},
        }

    def get_error_message(self, response_body):
        # renders the coming amadous response error to fit the custom
        # response error representation
        if self.is_amadaus_response():
            return self.render_amadous_error_response(response_body)

        error_tuple = namedtuple("error_tuple", ["key", "value"])

        # returns the resposnse_body if it's a single error message
        # else if response_body is a list of errors than turn
        # the key and value pairs into a tuples and return the first
        # tuple in the list
        err = (
            response_body
            if type(response_body) is str
            else [
                error_tuple(k, v if not type(v) is list else v[0])
                for k, v in response_body.items()
            ][0]
        )

        if isinstance(err, error_tuple):
            if err.value.__class__.__name__ == ErrorDetail.__name__:
                err._replace(value=str(err.value))

        finalized_error_msg = (
            err if type(err) is not error_tuple else err.value
        )

        return finalized_error_msg

    def is_amadaus_response(self):
        if hasattr(self.response, "is_amadaus"):
            if self.response.is_amadaus:
                return True
        return False

    def render_amadous_error_response(self, data):
        errs = data["errors"][0]

        key = ""
        body = errs["detail"]

        try:
            for char in errs["source"]["parameter"]:
                if char.isupper():
                    key += "_"
                    key += char.lower()
                    continue
                key += char
        except Exception:
            pass

        return {"key": key, "body": body}
