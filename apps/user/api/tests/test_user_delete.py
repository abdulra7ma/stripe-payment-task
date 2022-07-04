# Django imports
from django.urls import reverse

# external imports
from user.models import User

# app imports
from lib.utils.testing.core import CoreAPITestCase


class UserDeleteTestCase(CoreAPITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # generate a user object and activate it
        cls.user_saved = cls.factory.create(password="qwerty1234")

        cls.user_url = reverse("user-api")

    def test_user_existence_in_db_before_delete_request(self):
        """
        Check existence of the `user_saved` object before requesting
        resoure deletion, and the total number user objects in the db
        """
        user = User.objects.filter(id=self.user_saved.id)

        self.assertTrue(user.exists())
        self.assertEqual(User.objects.all().count(), 2)

    def test_delete_user_if_user_exists(self):
        """
        Request resourse deletion, check the response status code,
        and ensure the deletion of the resourse be checking the total
        user objects in the db
        """
        # provide JWT auth header
        self.provide_authorization_credentials()

        response = self.client.delete(self.user_url)

        self.assertEqual(response.status_code, self.status.HTTP_200_OK)
        self.assertEqual(User.objects.all().count(), 1)

    def get_credentials(self):
        credintails = {
            "email": self.user_saved.email,
            "password": "qwerty1234",
        }
        return credintails
