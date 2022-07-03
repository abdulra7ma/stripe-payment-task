"""
####################
    API Response
####################

a module

"""

# external imports
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


# class CustomRenderer(JSONRenderer):
#     """Custom JSON renderer for success and error response"""

#     RESPONSE = {
#         "message": "",
#         "status": {
#             "code": "",
#             "message": "",
#         },
#         "data": {},
#     }

#     def render(
#         self,
#         response_data,
#         accepted_media_type=None,
#         renderer_context=None,
#     ):
#         data = None if not "data" in response_data else response_data["data"]
#         message = (
#             response_data["message"] if "message" in response_data else None
#         )
#         status_code = renderer_context["response"].status_code
#         status_message = (
#             response_data["status_message"]
#             if "status_message" in response_data
#             else None
#         )

#         if str(status_code).startswith("2"):
#             response = self.success_response(
#                 message,
#                 status_code,
#                 status_message,
#             )
#         else:
#             if type(response_data) is dict:
#                 error = {k: str(v[0]) for k, v in response_data.items()}
#                 error = response_data
#             else:
#                 error = response_data
#             response = self.error_response(
#                 error,
#                 status_code,
#                 status_message,
#             )

#         return super(CustomRenderer, self,).render(
#             response,
#             accepted_media_type,
#             renderer_context,
#         )

#     def success_response(
#         self,
#         data,
#         status_code,
#         status_message=None,
#     ):
#         success_response = self.get_response_dict

#         success_response["message"] = status_message
#         success_response["data"] = data
#         success_response["success"] = True
#         success_response["status"]["code"] = status_code
#         success_response["status"]["message"] = status_message

#         return success_response

#     def error_response(
#         self,
#         data,
#         status_code,
#         status_message=None,
#     ):
#         error_response = self.get_response_dict

#         error_response["message"] = data
#         error_response["data"] = {}
#         error_response["error"] = True
#         error_response["status"]["code"] = status_code
#         error_response["status"]["message"] = data

#         return error_response


# def api_success(
#     *,
#     headers=None,
#     status=None,
#     message=None,
#     status_code=None,
#     status_message=None,
#     data=None
# ):
#     """
#     ############################
#         API Success Response
#     ############################

#     a function that shapes the response object of a
#     successful request returned to the client side
#     to ensure consistency accross the entire
#     application.


#     @param: headers        ->
#     @param: status         ->
#     @param: message        ->
#     @param: status_code    ->
#     @param: status_message ->

#     return: Response object composed of the following properties

#     @prop: headers ->
#     @prop: status ->
#     @prop: data ->

#     """
#     data = {
#         "message": message,
#         "status": {
#             "code": status_code,
#             "message": status_message,
#         },
#         "body": data,
#     }
#     return Response(
#         headers=headers,
#         status=status,
#         data=data,
#     )


# def api_error(
#     *,
#     headers=None,
#     status=None,
#     message=None,
#     status_code=None,
#     status_message=None
# ):

#     """
#     ##########################
#         API Error Response
#     ##########################

#     a function that shapes the response object of a
#     failed request returned to the client side
#     to ensure consistency accross the entire
#     application.


#     @param: headers ->
#     @param: status ->
#     @param: message ->
#     @param: status_code ->
#     @param: status_message ->

#     return: Response object composed of the following properties

#     @prop: headers ->
#     @prop: status ->
#     @prop: data ->

#     """

#     data = {
#         "error": message,
#         "status_code": status_code,
#         "message": status_message,
#     }
#     return Response(
#         headers=headers,
#         status=status,
#         data=data,
#     )


class Response(Response):
    """
    custom reseponse class that adds status_message and is_amadaus attributes
    to facilitate the debugging process and error customiztion
    """

    def __init__(
        self,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
        status_message=None,
        is_amadaus=False
    ):
        super().__init__(
            data, status, template_name, headers, exception, content_type
        )
        self.status_message = status_message
        self.is_amadaus = is_amadaus
