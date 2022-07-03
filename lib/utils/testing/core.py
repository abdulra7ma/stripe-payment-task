# Python imports
import string
from random import choice

# Django imports
from django.urls import reverse

# external imports
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, APITransactionTestCase

# app imports
from apps.authentication.api.tests.factory import UserFactory


class CoreTestCase:
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # initailize the api client for making requests
        cls.client = APIClient()

        # setup the token endpoint
        cls.token_url = reverse("token_obtain_pair")

        # setup status codes
        cls.status = status

        # setup User factory
        cls.factory = UserFactory

        # base user password
        cls.base_user_pass = cls().get_password()

        # setup the base user
        cls.base_user = cls.factory.create(password=cls.base_user_pass)

    def provide_authorization_credentials(self):
        """
        provides JWT authorization header
        """

        tokens = self.get_tokens

        tokens = self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + tokens["access"]
        )
        return tokens

    @property
    def get_tokens(self):
        """
        gets access and refresh tokens
        """

        tokens = self.client.post(self.token_url, data=self.get_credentials())
        return tokens.data

    def get_credentials(self, user=None):
        """
        returns login credentials
        """

        credintails = {
            "email": self.base_user.email if not user else user.email,
            "password": self.base_user_pass,
        }

        return credintails

    def get_password(self, length=10):
        letters = (
            string.ascii_letters
            + string.ascii_uppercase
            + string.ascii_letters
            + str(string.digits)
        )
        return "".join(choice(letters) for _ in range(length))


class CoreAPITestCase(CoreTestCase, APITestCase):
    """
    Custom API test case class
    that inherts both CoreTestCase and APITestCase.
    """


class CoreAPITransactionTestCase(CoreTestCase, APITransactionTestCase):
    """
    Custom transaction API test case class
    that inherts both CoreTestCase and APITransactionTestCase.
    """
