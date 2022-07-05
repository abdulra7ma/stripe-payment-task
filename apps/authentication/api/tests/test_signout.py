# Django imports
from django.urls import reverse

# external imports
import pytest
from rest_framework import status

# app imports
from lib.utils.testing.core import CoreAPITestCase

# app imports
from .factory import UserFactory

pytestmark = pytest.mark.django_db
logout_url = reverse("signout-api")


class UserLogOutTestCase(CoreAPITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_obj = UserFactory.build(password="asma3-meni-elsa3de")

        cls.user_password = cls().get_password()

        # generate a user object and activate it
        cls.user_saved = UserFactory.create(password=cls.user_password)

        # define the login endpoint
        # example -> {current-domian}/api/auth/login
        cls.logout_url = reverse("signout-api")

        # define the token endpoint, to get the refresh and access tokens
        cls.token_url = reverse("token_obtain_pair")

    def test_logout_user(self):
        self.provide_authorization_credentials()

        # get the refresh and access tokens
        tokens = self.get_tokens

        # post request to the sign-out url with refresh token as the given data
        response = self.client.post(
            self.logout_url, data={"token": tokens["refresh"]}
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # post request to with the same refresh token to get 400 error code
        response = self.client.post(
            self.logout_url, data={"token": tokens["refresh"]}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertAlmostEqual(response.data, "Token is blacklisted")

    @property
    def get_auth_token(self):
        credentials = {
            "email": self.user_saved.email,
            "password": "qwerty1234",
        }
        token = self.client.post(self.token_url, data=credentials)
        return token.data

    def get_credentials(self, user=None):
        credentials = super().get_credentials(user=self.user_saved)
        credentials["password"] = self.user_password
        return credentials


def get_tokens(client):
    """
    gets access and refresh tokens
    """
    token_url = reverse("token_obtain_pair")
    tokens = client.post(token_url, data=self.get_credentials())
    return tokens.data


def test_logout_user(client):
    self.provide_authorization_credentials()

    # get the refresh and access tokens
    tokens = self.get_tokens

    # post request to the sign-out url with refresh token as the given data
    response = client.post(logout_url, data={"token": tokens["refresh"]})

    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # post request to with the same refresh token to get 400 error code
    response = self.client.post(
        self.logout_url, data={"token": tokens["refresh"]}
    )

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertAlmostEqual(response.data, "Token is blacklisted")
