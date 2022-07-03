# Django imports
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

# external imports
from user.models import User
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

# app imports
from apps.authentication.utils.token import (
    serializer_validate_token,
    validate_token,
)
from apps.base.serializers.core import CoreModelSerializer, CoreSerializer
from apps.base.serializers.helpers import (
    serializer_error_messages,
)

# app imports
from ..utils.constants import AuthConst, SerializerConst


class LoginSerializer(CoreSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    def validate(self, data):
        """
        checks user exists and password is correct.
        """

        try:
            User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError(SerializerConst.INVALID_EMAIL)

        authenticated_user = authenticate(
            request=self.context["request"],
            username=data["email"],
            password=data["password"],
        )

        if not authenticated_user:
            raise AuthenticationFailed(AuthConst.INVAILD_CRED)

        return data


class RegisterationSerializer(CoreModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        trim_whitespace=False,
        error_messages={
            **serializer_error_messages("password", min_lenght=True)
        },
        min_length=8,
    )
    password_confirmation = serializers.CharField(
        write_only=True,
        required=True,
        trim_whitespace=False,
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "password_confirmation",
        )

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(AuthConst.ALREADY_EXISTS)
        return email

    def validate(self, attrs):
        """check `password_confirmation` field if not equal `password` field"""

        if attrs["password_confirmation"] != attrs["password"]:
            raise serializers.ValidationError(
                SerializerConst.INVALID_PASSWORD_CONFIRM
            )
        return attrs

    def create(self, validated_data):
        del validated_data["password_confirmation"]

        # get `email` and password data from `validated_data`
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        # create user instance
        instance = User.objects.create_user(
            email, password, **validated_data
        )

        return instance


class PasswordRestSerializer(CoreSerializer):
    new_password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
        required=True,
        validators=[validate_password],
        error_messages={
            **serializer_error_messages(
                "new_password", min_lenght=True
            )
        },
        min_length=8,
    )
    confirm_password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    def validate(self, attrs):
        if attrs["confirm_password"] != attrs["new_password"]:
            raise serializers.ValidationError(
                SerializerConst.INVALID_PASSWORD_CONFIRM
            )
        return attrs


class ForgertPasswordRestSerializer(CoreSerializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
        required=True,
        validators=[validate_password],
        error_messages={
            **serializer_error_messages(
                "new_password", min_lenght=True
            )
        },
        min_length=8,
    )
    confirm_password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    def validate_token(self, token_string):
        token = validate_token(token_string)
        return token

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                SerializerConst.INVALID_PASSWORD_CONFIRM
            )
        return attrs


class FindUserByEmailSerializer(CoreSerializer):
    """
    This serializer will find user by email. If the user doesn't exist,
    raise validation error
    """

    email_address = serializers.EmailField(required=True)

    def validate(self, attrs):
        try:
            User.objects.get(email=attrs["email_address"])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                SerializerConst.DOESNOT_EXISTS_USER
            )
        return super().validate(attrs)
    
    @property
    def user(self):
        return User.objects.get(email=self.validated_data["email_address"])

class ChangeEmailSerializer(CoreSerializer):
    new_email_address = serializers.EmailField(
        required=True,
    )

    def validate(self, attrs):
        if User.objects.filter(email=attrs["new_email_address"]).exists():
            raise serializers.ValidationError(SerializerConst.EMAIL_EXISTS)
        return attrs


class SignOutRefreshTokenSerializer(CoreSerializer):
    token = serializers.CharField(required=True)

    def validate_token(self, token):
        return serializer_validate_token(token)
