# Django imports
from django.utils.translation import gettext_lazy as _


class SuccessMessage:
    """docstring for SuccessMessage."""

    """ ACCOUNT """
    ACCOUNT_CREATED =  _("Successfully created account")
    ACCOUNT_RETREIVED = _("Successfully retreived account")
    ACCOUNT_UPDATED = _("Successfully updated account")
    ACCOUNT_ACTIVATED = _("Successfully activated account")
    ACCOUNT_DEACTIVATED = _("Successfully deactivated account")
    ACCOUNT_DELETED = _("Successfully deleted account")

    """ AUTH """
    SIGNED_IN = _("Successfully signed In")
    SIGNED_OUT = _("Successfully signed Out")

    """ OBJECT """
    OBJECT_RETRIEVED = _("Successfully OBJECT retrieved")
    OBJECTS_RETRIEVED = _("Successfully OBJECTs retrieved")
    OBJECT_PURCHASED = _("Successfully OBJECT purchased")

    """ PAYMENT """
    PAYMENT_PROCESSED = _("Successfully payment processed")

    """ Django Models """
    RETRIEVED = _("Successfully retrieved")
    CREATED = _("Successfully created")
    UPDATED = _("Successfully updated")
    DELETED = _("Successfully deleted")


class ErrorMessage:
    """docstring for ErrorMessage."""

    """ ACCOUNT """
    FAILED_TO_CREATE_ACCOUNT = "Failed to create an account"

    """ AUTH """
    FAILED_TO_SIGN_IN = _("Failed to sign in")
    FAILED_TO_SIGN_OUT = _("Failed to sign out")
    ACTIVATION_LINK_EXPIRED = _("Activations link expired")

    """ OBJECT """
    FAILED_TO_RETRIEVE_OBJECT = _("Failed to retrieve OBJECT")
    FAILED_TO_PURCHASE_OBJECT = _("Failed to purchase OBJECT")
    FAILED_TO_RETRIEVE_OBJECTS = _("Failed to retrieve OBJECTs")
    FAILED_TO_PURCHASE_OBJECTS = _("Failed to purchase OBJECTs")

    """ PAYMENT """
    FAILED_TO_PROCESS_PAYMENT = _("Failed to process payment")

    """ Token """
    TOKEN_BLACKLISTED = _("This token is blacklisted")


success_message = SuccessMessage()
error_message = ErrorMessage()