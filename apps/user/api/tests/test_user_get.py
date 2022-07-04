# Django imports
from django.urls import reverse

# external imports
from authentication.api.tests.factory import UserFactory
from rest_framework import status
from rest_framework.test import APIClient

# app imports
from lib.utils.testing.core import CoreAPITestCase


class UserGetTestCase(CoreAPITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_obj = UserFactory.build(password="user")

        # generate a user object and activate it
        cls.user_saved = UserFactory.create(password="qwerty1234")

        # initail the api client for making requests
        cls.client = APIClient()
        cls.user_url = reverse("user-api")
        cls.token_url = reverse("token_obtain_pair")

    def get_token(self):
        credintails = {
            "email": self.user_saved.email,
            "password": "qwerty1234",
        }
        tokens = self.client.post(self.token_url, data=credintails)
        return tokens.data["access"]

    def test_authorized_get_request(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.get_token()
        )
        response = self.client.get(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["user"]["first_name"], self.user_saved.first_name
        )
