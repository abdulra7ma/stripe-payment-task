# Django imports
from django.urls import reverse

# external imports
from faker import Faker
from rest_framework import status

# app imports
from lib.utils.testing.core import CoreAPITestCase

from user.models import User

# app imports
from .factory import UserFactory


class UserSignUpTestCase(CoreAPITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_password = cls().get_password()

        cls.user_object = UserFactory.build(password=cls.user_password)
        cls.user_saved = UserFactory.create(password=cls.user_password)

        cls.signup_url = reverse("register-api")
        cls.faker_obj = Faker()

    def test_if_data_is_correct_then_signup(self):
        # Prepare data
        signup_dict = {
            "email": self.user_object.email,
            "password": self.user_password,
            "password_confirmation": self.user_password,
        }

        # Make request
        response = self.client.post(self.signup_url, signup_dict)

        # Check status response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

        # Check database
        new_user = User.objects.get(email=self.user_object.email)

        self.assertEqual(new_user.email, self.user_object.email)

    def test_already_signed_up_user(self):
        # Prepare data
        signup_dict = {
            "email": self.user_saved.email,
            "password": "test_Pass",
            "password_confirmation": "test_Pass",
        }

        # Make request
        response = self.client.post(self.signup_url, signup_dict)

        # Check status response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
