# Django imports
from django.contrib.sites.models import Site
from django.urls import reverse

# external imports
from celery import shared_task
from decouple import config
from rest_framework_simplejwt.tokens import RefreshToken

# app imports
from core.celery import app
from lib.utils.tokens.core import (
    ActivationToken,
    ChangeEmailToken,
    DeactivationToken,
    PasswordResetToken,
)

# app imports
from .utils.email_threads import EmailThread


class EmailSender:
    def __init__(self, reciever) -> None:
        self.reciever = reciever

    def send_mail(self, subject, email_body, to):
        # initiate an email thread
        EmailThread(
            subject=subject, recipient=to, html_content=email_body
        ).start()

    def email_activation(self):
        """Sends activation email to the new signing user"""

        # generate account activation token
        token = ActivationToken.for_user(self.reciever)
        subject = "Verify your email"
        body = (
            "Hi "
            + self.reciever.email
            + " Use the link below to verify your email \n"
            + (self.get_absolute_url("email-verify") + "?token=" + str(token))
        )
        self.send_mail(subject, body, self.reciever.email)
        return True

    def email_deactivation(self):
        """Sends deactivation email to the current activated user"""
        # generate account activation token
        token = DeactivationToken.for_user(self.reciever)
        subject = "Deactivate your email"
        body = (
            "Hi "
            + self.reciever.email
            + " Use the link below to deactivate your email \n"
            + (
                self.get_absolute_url("account-deactivate-execute")
                + "?token="
                + str(token)
            )
        )
        self.send_mail(subject, body, self.reciever.email)
        return True

    def email_password_rest(self):
        """Sends password reset email"""

        # generate account activation token
        token = PasswordResetToken.for_user(self.reciever)
        subject = "Reset your password"
        body = (
            "Hi "
            + self.reciever.email
            + " Use the link below to reset your password \n"
            + (
                self.get_absolute_url("forgot-password-confirm")
                + "?token="
                + str(token)
            )
        )
        self.send_mail(subject, body, self.reciever.email)
        return True

    def email_change_email(self):
        """Sends change reset email to the current signed user"""
        # generate account activation token
        token = ChangeEmailToken.for_user(self.reciever)
        subject = "Change your email"
        body = (
            "Hi "
            + self.reciever.email
            + " Use the link below to deactivate your email \n"
            + (
                self.get_absolute_url("change-email-execute")
                + "?token="
                + str(token)
            )
        )
        self.send_mail(subject, body, self.reciever.email)
        return True

    def get_absolute_url(self, endpoint_url_name) -> str:
        front_end_absolute_urls = {}
        environ = config("ENV", default="development", cast=str)

        if environ == "development":
            site, _ = Site.objects.get_or_create(
                name="development", domain="127.0.0.1:8000"
            )
            return "http://" + str(site.domain) + reverse(endpoint_url_name)
        elif environ == "production":
            pass

        return ""


def send_mail(subject, email_body, to):
    # initiate an email thread
    EmailThread(subject=subject, recipient=to, html_content=email_body).start()


@shared_task(serializer="pickle")
def send_email_activation_link(user, email, site_domain):
    """
    Sends activation email to the new signing user

    Arguments:
        email (str): the new sign up user email

    Return:
        bool: pass

    """

    # generate account activation token
    token = ActivationToken.for_user(user)

    relativeLink = "/auth"

    # activation url
    absurl = site_domain + relativeLink + "?token=" + str(token)
    email_body = (
        "Hi "
        + user.full_name
        + " Use the link below to verify your email \n"
        + absurl
    )

    send_mail(subject="Verify your email", to=email, email_body=email_body)

    return True


@shared_task(serializer="pickle")
def send_email_deactivation_link(user, email, site_domain):
    """
    Sends deactivation email to the an exist user

    Arguments:
        email (str): exist user email

    Return:
        bool: pass

    """

    # generate account activation token
    token = DeactivationToken.for_user(user)

    # get the site domain
    current_site = site_domain

    relativeLink = reverse("account-deactivate")

    # activation url
    absurl = "http://" + current_site + relativeLink + "?token=" + str(token)
    email_body = (
        "Dear customer "
        + user.full_name
        + "\n\n"
        + " Use this link below to deactivate your account: \n"
        + absurl
    )

    send_mail(subject="Deactivate account", to=email, email_body=email_body)

    return "Successfully sended deactivation email"


@shared_task(serializer="pickle")
def send_email_password_rest(user, email, site_domain):
    # generate account activation token
    token = RefreshToken.for_user(user).access_token

    relativeLink = reverse("forgot-password-confirm")

    # activation url
    absurl = "http://" + site_domain + relativeLink + "?token=" + str(token)
    email_body = (
        "Dear customer "
        + user.full_name
        + "\n\n"
        + " Use this link below to reset your account password: \n"
        + absurl
    )

    send_mail(subject="Reset Password", to=email, email_body=email_body)

    return True


@shared_task(bind=True)
def send_email_change_email(user, email, site_domain):
    # generate account activation token
    token = ChangeEmailToken.for_user(user)

    relativeLink = reverse("change-email")

    # activation url
    absurl = "http://" + site_domain + relativeLink + "?token=" + str(token)
    email_body = (
        "Dear customer "
        + user.full_name
        + "\n\n"
        + " Use this link below to chaneg your account email: \n"
        + absurl
    )

    send_mail(subject="Change Email", to=email, email_body=email_body)

    return True
