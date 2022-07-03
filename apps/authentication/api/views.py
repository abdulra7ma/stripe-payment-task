# Python imports
import ast

# Django imports
from django.conf import UserSettingsHolder, settings
from django.contrib.sites.shortcuts import get_current_site

# external imports
import jwt
from user.api.serializers import (
    UserSerializer,
    UserPicResponceSerializer,
)
from user.models import User, UserPic
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

# app imports
from apps.authentication.utils.token import validate_token, verify_email_token
from lib.constants.api.messages import error_message, success_message
from lib.exceptions.core import InvaildToken
from lib.loggers.logger import Logger
from lib.services.email.email import (
    EmailSender,
    send_email_activation_link,
    send_email_change_email,
    send_email_deactivation_link,
    send_email_password_rest,
)
from lib.utils.api.response import Response
from lib.utils.tokens.token_helpers import get_jwt_token

# app imports
from ..models import LoginDevice
from ..utils.auth_helpers import (
    deactivate_account,
    delete_device,
    get_ip_address,
    get_user_agent,
    set_last_login,
)
from ..utils.constants import AuthConst
from ..utils.swagger import (
    email_address_param,
    login_response_schema_dict,
    token_param,
)
from .exceptions import CustomErrorException
from .serializers import (
    ChangeEmailSerializer,
    FindUserByEmailSerializer,
    ForgertPasswordRestSerializer,
    LoginSerializer,
    PasswordRestSerializer,
    RegisterationSerializer,
    SignOutRefreshTokenSerializer,
)

init_logger = Logger("auth_logger")
logger = init_logger()


class Register(generics.GenericAPIView):
    serializer_class = RegisterationSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """Register/Create new user and activate the account automatically"""

        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # get serialized email data
        email = serializer.data["email"]

        # get the new created user and activate it
        user = User.objects.get(email=email)

        # activate the new registerted user
        user.is_active = True
        user.save()

        # generate account access token
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        # send activation email
        email_sender = EmailSender(user)
        email_sender.email_activation()

        return Response(
            data={
                "tokens": {
                    "access": str(access_token),
                    "refresh": str(refresh_token),
                },
                "user": UserSerializer(instance=user).data,
            },
            status=status.HTTP_201_CREATED,
            status_message=success_message.ACCOUNT_CREATED,
        )

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class LogIn(generics.GenericAPIView):
    serializer_class = LoginSerializer
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses=login_response_schema_dict)
    def post(self, request, *args, **kwargs):
        data = request.data
        login_serializer = self.get_serializer(data=data)

        if not login_serializer.is_valid():
            raise CustomErrorException(
                detail=self.serialize_error(login_serializer.errors),
                code="invaild_credentials",
                status_code=401,
            )

        user = User.objects.get(email=login_serializer.data.get("email"))
        self.login(request, user)

        user_pic_obj, created = UserPic.objects.get_or_create(user=user)

        # generate account access token
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        return Response(
            data={
                "tokens": {
                    "access": str(access_token),
                    "refresh": str(refresh_token),
                },
                "user": UserSerializer(instance=user).data,
            },
            status=status.HTTP_200_OK,
            status_message=success_message.SIGNED_IN,
        )

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """

        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()

        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def login(self, request, user):
        ip_address = get_ip_address(request)
        (device, os, browser) = get_user_agent(request)

        (login_device, _) = LoginDevice.objects.get_or_create(
            user=user,
            device=device,
            os=os,
            browser=browser,
            ip_address=ip_address,
        )

        set_last_login(login_device)
        return login_device

    def serialize_error(self, errs):
        for err in errs:
            errs[err] = errs[err][0]
        return errs


class Logout(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SignOutRefreshTokenSerializer

    def post(self, request, *args, **kwargs):
        """
        Logout a user by blacklisting his refresh token. This view needs to recieve
        a refresh token in order to blacklist it, so it will not be vaild to be used
        any more.
        """

        ip_address = get_ip_address(request)
        (device, os, browser) = get_user_agent(request)

        # logging the current device of the user
        login_device = LoginDevice.objects.filter(
            user=request.user,
            device=device,
            os=os,
            browser=browser,
            ip_address=ip_address,
        ).first()

        # delete user's current logging device
        delete_device(login_device)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token = RefreshToken(serializer.data["token"])
            token.blacklist()
        except TokenError as e:
            # if the token is blacklisted than it will raise TokenError.
            return Response(
                str(e),
                status=status.HTTP_400_BAD_REQUEST,
                status_message=error_message.TOKEN_BLACKLISTED,
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            status_message=success_message.SIGNED_OUT,
        )


class VerifyEmail(APIView):
    """
    API View for email verification using JWT access token
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """
        Verifies coming token and deactivate the user account

        Workflow:
            1. extract token from the request url
            2. varifies the token
            3. get related user account object by using the payload user_id
            4. deactive account

        Return:
            if token valid:
                (response): return 200 succuss response
            else:
                (exception): raise exception if the link is expired
        """

        token = get_jwt_token(request)
        payload = validate_token(token)

        # get the user instance by the extracted user_id from the token payload
        user = User.objects.get(id=payload["user_id"])

        if not user.is_active:
            user.is_active = True
            user.save()

        return Response("Successfully activated", status=status.HTTP_200_OK)


class ChangeEmailRequest(APIView):
    """
    Send change request email to current authenticated user
    """

    def get(self, request, *args, **kwargs):
        # send change_email email
        email_sender = EmailSender(request.user)
        email_sender.email_change_email()

        return Response(
            data="Successfully send the email. Please check your email",
            status=status.HTTP_200_OK,
        )


class ChangeEmailExecute(APIView):
    """
    Verify coming url token and change the token' user email
    """

    permission_classes = []
    authentication_classes = []
    serializer_class = ChangeEmailSerializer

    @swagger_auto_schema(
        manual_parameters=[token_param], request_body=ChangeEmailSerializer
    )
    def post(self, request, *args, **kwargs):
        token = get_jwt_token(request)
        payload = self.validate_token(token)

        # validate the coming email address
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # replace the current email with the new email
        user = UserSettingsHolder.objects.get(id=payload["user_id"])
        user.email = serializer.data["new_email_address"]
        user.save()

        return Response(
            "Successfully changed email", status=status.HTTP_200_OK
        )

    def validate_token(self, token):
        try:
            payload = jwt.decode(
                token,
                key=settings.SECRET_KEY,
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError as e:
            raise InvaildToken("link expired", code="link_expired")
        except jwt.exceptions.DecodeError as e:
            raise InvaildToken("Invalid Link", code="link_token")

        return payload


class DeactivateAccountRequest(APIView):
    """
    Send deactivation email to the current authenticated user

    Return:
            if user active:
                (response): return 200 succuss response
            elif user is not active:
                (response): return 400 bad request
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # send deactivation email
        email_sender = EmailSender(request.user)
        email_sender.email_deactivation()

        # send deactivation email
        # send_email_deactivation_link.apply_async(
        #     args=(request.user, user_email, get_current_site(request).domain)
        # )

        return Response(
            AuthConst.EMAIL_DEACTIVATE,
            status=status.HTTP_200_OK,
        )

    def check_object_permissions(self, request, obj):
        if not self.request.user.is_active:
            return Response(
                AuthConst.ALREADY_DEACTIVATED,
                status=status.HTTP_400_BAD_REQUEST,
            )


class DeactivateAccountExecute(APIView):
    """
    Verifies coming token and deactivate user account

    Return:
        if token valid:
            (response): return 204 succuss response
        else:
            (exception): raise exception if the link is expired
    """

    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        token = get_jwt_token(request)
        payload = validate_token(token)

        # get the user instance by the extracted
        # user_id from the token payload
        user = User.objects.get(id=payload["user_id"])

        # deactivate the user account
        deactivate_account(user)

        return Response(
            AuthConst.DEACTIVATE,
            status=status.HTTP_204_NO_CONTENT,
        )


class PasswordResetRequest(APIView):
    """
    Takes an email_address query argument, then it sends an email \
        to the user if the user email is valid.

    Accepts:
        email_address: String

    Return
        status 200
    """

    serializer_class = FindUserByEmailSerializer
    authentication_classes = []
    permission_classes = []

    def get_email_query_param(self):
        email = self.request.query_params.get("email_address")
        if not email:
            raise APIException(
                detail="email_address query param not provided within the url",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return email

    @swagger_auto_schema(manual_parameters=[email_address_param])
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # send_email_password_rest.apply_async(
        #     args=(
        #         serializer.user,
        #         serializer.data["email_address"],
        #         get_current_site(request).domain,
        #     )
        # )

        # send password reset email
        email_sender = EmailSender(serializer.user)
        email_sender.email_password_rest()

        return Response(status=status.HTTP_200_OK)


class ChangePassword(APIView):
    """
    Set a new password for an authenticated user
    """

    serializer_class = PasswordRestSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data["confirm_password"])
        user.save()

        return Response(
            AuthConst.PASSWORD_REST,
            status=status.HTTP_200_OK,
        )


class PasswordResetExecute(APIView):
    """
    Validate token and Reset password
    """

    serializer_class = ForgertPasswordRestSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # generate data for serializer
        data = {k: v for k, v in request.data.items()}
        data["token"] = get_jwt_token(request)

        # serialize the given data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        token = ast.literal_eval(serializer.data["token"])
        user = self.get_user(token["user_id"])

        # set new password
        user.set_password(serializer.validated_data["confirm_password"])
        user.save()

        return Response(
            AuthConst.PASSWORD_REST,
            status=status.HTTP_200_OK,
        )

    def get_user(self, id):
        return User.objects.get(id=id)


class VerifyToken(APIView):
    """
    Verify the coming token
    """

    def get(self, request, *args, **kwargs):
        token = get_jwt_token(request)
        payload = verify_email_token(token)
        return Response(status=status.HTTP_200_OK)
