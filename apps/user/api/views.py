# external imports
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, status
from rest_framework.exceptions import APIException
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

# app imports
from ..models import User
from .serializers import (
    UserPicSerializer,
    UserSerializer,
    UserUpdateModelSerializer,
)


class UserAPIView(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.RetrieveAPIView,
):
    """
    Create, Update, Retrieve and Delete User instance.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "PATCH" or self.request.method == "PUT":
            self.serializer_class = UserUpdateModelSerializer
        return self.serializer_class

    def get_object(self):
        """Get User instance from the access token"""
        return self.request.user

    def get(self, request, *args, **kwargs):
        """
        Gets current authenticated user object
        """

        return Response(
            data={
                "user": UserSerializer(instance=self.get_object()).data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, *args, **kwargs):
        """
        Deletes current authenticated user object
        """

        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """
        Updates current authenticated user object
        """

        instance = self.get_object()
        serializer = self.serializer_class(
            data=request.data, partial=True, instance=instance
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class UserImageAPIView(APIView):
#     parser_classes = (MultiPartParser, FileUploadParser)
#     serializer_class = UserPicSerializer

#     def get(self, request, *args, **kwargs):
#         """
#         Gets current user profile Image
#         """

#         serializer = self.serializer_class(instance=self.get_user_pic_object())
#         return Response(data=serializer.data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         operation_description="Upload user profile image",
#         operation_id="Upload user profile image",
#         manual_parameters=[
#             openapi.Parameter(
#                 name="file",
#                 in_=openapi.IN_FORM,
#                 type=openapi.TYPE_FILE,
#                 required=True,
#                 description="Document",
#             )
#         ],
#         responses={400: "Invalid data in uploaded file", 200: "Success"},
#     )
#     def post(self, request, format=None):
#         """
#         Uploades current user profile Image
#         """
#         # delete old profile picture, if exists
#         user_profile_pic = UserPic.objects.filter(user=request.user)
#         user_profile_pic.delete()

#         data = {"picture": self.get_image_file(), "user": request.user.id}
#         serialzer = self.serializer_class(data=data)
#         if serialzer.is_valid():
#             serialzer.save()
#             return Response(serialzer.data, status=status.HTTP_200_OK)

#         return Response(
#             data="Failed to uplaod the image",
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     @swagger_auto_schema(
#         operation_description="Update user profile image",
#         operation_id="Update user profile image",
#         manual_parameters=[
#             openapi.Parameter(
#                 name="file",
#                 in_=openapi.IN_FORM,
#                 type=openapi.TYPE_FILE,
#                 required=True,
#                 description="Document",
#             )
#         ],
#         responses={400: "Invalid data in uploaded file", 200: "Success"},
#     )
#     def patch(self, request, *args, **kwargs):
#         """
#         Updates current user profile Image
#         """

#         serilizer = self.serializer_class(
#             instance=self.get_user_pic_object(),
#             data={
#                 "picture": self.get_image_file(),
#             },
#             partial=True,
#         )
#         if serilizer.is_valid():
#             serilizer.save()
#             return Response(data=serilizer.data, status=status.HTTP_200_OK)

#         return Response(
#             data=serilizer.errors, status=status.HTTP_400_BAD_REQUEST
#         )

#     def delete(self, request, *args, **kwargs):
#         """
#         Deletes current user profile Image
#         """
#         user_pic = self.get_user_pic_object()
#         user_pic.delete()
#         return Response(status=status.HTTP_200_OK)

#     def get_image_file(self):
#         img_file = self.request.data.get("file", None)
#         if not img_file:
#             raise APIException(detail="Please upload an image file")
#         return img_file

#     def get_user_pic_object(self):
#         user_pic = UserPic.objects.filter(user=self.request.user)

#         if not user_pic.exists():
#             raise APIException(
#                 detail="User has no profile picture",
#                 code=status.HTTP_400_BAD_REQUEST,
#             )
#         return user_pic.first()
