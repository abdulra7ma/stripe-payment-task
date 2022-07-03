# Django imports
from django.urls import reverse

# external imports
from customer.models import Customer

# app imports
from lib.utils.testing.core import CoreAPITestCase


class CustomerGetTestCase(CoreAPITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer_object = cls.factory.build(password="customer")

        # generate a user object and activate it
        cls.customer_saved = cls.factory.create(password="qwerty1234")

        cls.customer_url = reverse("customer-api")

    def test_valid_patch_data(self):
        data = {
            "first_name": self.customer_object.first_name,
            "middle_name": self.customer_object.middle_name,
        }

        self.provide_authorization_credentials()

        # test the unvalid equivalence before the request
        self.assertNotEqual(data["first_name"], self.customer_saved.first_name)

        response = self.client.patch(self.customer_url, data=data)
        customer_obj = Customer.objects.get(id=self.customer_saved.id)

        self.assertEqual(response.status_code, self.status.HTTP_200_OK)

        # test the valid equivalence after the patch request.
        # These assert statements ensures the modification
        # of the requested resourse.
        self.assertEqual(response.data["first_name"], customer_obj.first_name)
        self.assertEqual(response.data["middle_name"], data["middle_name"])

    def get_credentials(self):
        credintails = {
            "email": self.customer_saved.email,
            "password": "qwerty1234",
        }
        return credintails
