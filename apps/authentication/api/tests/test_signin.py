# Django imports
from django.urls import reverse

# external imports
from rest_framework import status

# app imports
from lib.utils.testing.core import CoreAPITestCase

# app imports
from .factory import UserFactory


class UserLogInTestCase(CoreAPITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user_password = cls().get_password()

        cls.user_obj = UserFactory.build(password=cls.user_password)

        # generate a user object
        cls.user_saved = UserFactory.create(password=cls.user_password)

        # define the login endpoint
        # example -> {current-domian}/api/auth/login
        cls.login_url = reverse("login-api")

    def test_login_user_with_valid_credentials(self):
        credintails = {
            "email": self.user_saved.email,
            "password": self.user_password,
        }

        response = self.client.post(self.login_url, data=credintails)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_with_invalid_credentials(self):
        credintails = {
            "email": "gdsvfuvsdjfv",
            "password": "qwerty1234",
        }

        # login request
        response = self.client.post(self.login_url, data=credintails)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_uncorrect_password_and_email_fields(self):
        unvaild_pass_msg = "invaild credentials"
        unvaild_email_msg = "Invalid email address."

        credintails = {
            "email": self.user_obj.email,
            "password": "qwer1234",
        }

        # login request for the unvaild email error
        response = self.client.post(self.login_url, data=credintails)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # compare the `unvaild_email_msg` variable and
        # the returned unvaild email message
        self.assertEqual(response.data["non_field_errors"], unvaild_email_msg)

        # change the value of the `email` key to a vaild email
        credintails["email"] = self.user_saved.email

        # login request for the unvaild password error
        response = self.client.post(self.login_url, data=credintails)

        # compare the `unvaild_pass_msg` variable and
        # the returned unvaild password message
        self.assertEqual(response.data["detail"], unvaild_pass_msg)

    def test_empty_values_for_password_and_email(self):
        credintails = {"email": "", "password": ""}

        response = self.client.post(self.login_url, data=credintails)

        self.assertEqual(
            response.status_code, self.status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(response.data["email"], "Email may not be blank")
        self.assertEqual(response.data["password"], "Password may not be blank")
