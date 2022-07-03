# Django imports
from django.utils.translation import gettext_lazy as _


class AuthConstants:
    INVAILD_CRED = _("invaild credentials")
    LOG_OUT = _("Successfully logged out.")
    PASSWORD_REST = _("Successful Password reset")
    ALREADY_DEACTIVATED = _("User already deactivated")
    DEACTIVATE = _("Successfully deactivated")
    EMAIL_DEACTIVATE = _("Check your email to Confirm account deactivation")
    INVALID_PASSWORD = _("Password is incorrect.")
    ALREADY_EXISTS = _("This email can not be used. Please use another email")


class SerializerConstants:
    INVALID_EMAIL = _("Invalid email address.")
    INVALID_PASSWORD_CONFIRM = _(
        "Password confirmation does not match the initail password"
    )
    DOESNOT_EXISTS_USER = _("User with given email does not exists")
    EMAIL_EXISTS = _("This email can not be used please try another email.")


class TokenConstants:
    EXPIRED = "Token Expired"
    INVALID = "Invlid Token"
    EXPIRED_DEACTIVATION_LINK = "Deactivation link expired"
    EXPIRED_ACTIVATION_LINK = "Activation link expired"
    USED = ""


AuthConst = AuthConstants()
SerializerConst = SerializerConstants()
TokenConst = TokenConstants()
