# Django imports
from django.urls import path

# app imports
from .views import (
    ChangeEmailExecute, ChangeEmailRequest, ChangePassword,
    DeactivateAccountExecute, DeactivateAccountRequest, LogIn, Logout,
    PasswordResetExecute, PasswordResetRequest, Register, VerifyEmail,
    VerifyToken,
)

urlpatterns = [
    path("/sign-up", Register.as_view(), name="register-api"),
    path("/sign-in", LogIn.as_view(), name="login-api"),
    path("/sign-out", Logout.as_view(), name="signout-api"),
    path("/email/verify", VerifyEmail.as_view(), name="email-verify"),
    path(
        "/account/deactivate/request",
        DeactivateAccountRequest.as_view(),
        name="account-deactivate-request",
    ),
    path(
        "/account/deactivate/execute",
        DeactivateAccountExecute.as_view(),
        name="account-deactivate-execute",
    ),
    path(
        "/password/reset/request",
        PasswordResetRequest.as_view(),
        name="forgot-password",
    ),
    path(
        "/password/reset/execute",
        PasswordResetExecute.as_view(),
        name="forgot-password-confirm",
    ),
    path("/password/change", ChangePassword.as_view(), name="reset-password"),
    path(
        "/email/change/request",
        ChangeEmailRequest.as_view(),
        name="change-email-request",
    ),
    path(
        "/email/change/execute",
        ChangeEmailExecute.as_view(),
        name="change-email-execute",
    ),
    # path("token/verify", VerifyToken.as_view(), name="token-verify"),
]
