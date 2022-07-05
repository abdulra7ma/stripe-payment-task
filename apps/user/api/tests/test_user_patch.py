# Django imports
from django.urls import reverse

# external imports
from user.models import User

# app imports
from lib.utils.testing.core import CoreAPITestCase

import pytest

pytestmark = pytest.mark.django_db


class UserGetTestCase(CoreAPITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_object = cls.factory.build(password="user")

        # generate a user object and activate it
        cls.user_saved = cls.factory.create(password="qwerty1234")

        cls.user_url = reverse("user-api")

    def test_valid_patch_data(self):
        data = {
            "first_name": self.user_object.first_name,
            "middle_name": self.user_object.middle_name,
        }

        self.provide_authorization_credentials()

        # test the unvalid equivalence before the request
        self.assertNotEqual(data["first_name"], self.user_saved.first_name)

        response = self.client.patch(self.user_url, data=data)
        user_obj = User.objects.get(id=self.user_saved.id)

        self.assertEqual(response.status_code, self.status.HTTP_200_OK)

        # test the valid equivalence after the patch request.
        # These assert statements ensures the modification
        # of the requested resourse.
        self.assertEqual(response.data["first_name"], user_obj.first_name)
        self.assertEqual(response.data["middle_name"], data["middle_name"])

    def get_credentials(self):
        credintails = {
            "email": self.user_saved.email,
            "password": "qwerty1234",
        }
        return credintails
