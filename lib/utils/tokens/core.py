# Python imports
from datetime import timedelta

# external imports
from rest_framework_simplejwt.tokens import RefreshToken, Token


class ActivationToken(Token):
    token_type = "activation"
    lifetime = timedelta(minutes=10)


class DeactivationToken(Token):
    token_type = "deactivation"
    lifetime = timedelta(minutes=10)


class ChangeEmailToken(Token):
    token_type = "change-email"
    lifetime = timedelta(minutes=30)


class PasswordResetToken(Token):
    token_type = "password-reset"
    lifetime = timedelta(minutes=30)
