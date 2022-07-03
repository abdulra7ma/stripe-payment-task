# Django imports
from django.urls import reverse

# external imports
from customer.models import Customer

# app imports
from lib.utils.testing.core import CoreAPITestCase


class CustomerDeleteTestCase(CoreAPITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # generate a user object and activate it
        cls.customer_saved = cls.factory.create(password="qwerty1234")

        cls.customer_url = reverse("customer-api")

    def test_customer_existence_in_db_before_delete_request(self):
        """
        Check existence of the `customer_saved` object before requesting
        resoure deletion, and the total number Customer objects in the db
        """
        customer_object = Customer.objects.filter(id=self.customer_saved.id)

        self.assertTrue(customer_object.exists())
        self.assertEqual(Customer.objects.all().count(), 2)

    def test_delete_customer_if_customer_exists(self):
        """
        Request resourse deletion, check the response status code,
        and ensure the deletion of the resourse be checking the total
        Customer objects in the db
        """
        # provide JWT auth header
        self.provide_authorization_credentials()

        response = self.client.delete(self.customer_url)

        self.assertEqual(response.status_code, self.status.HTTP_200_OK)
        self.assertEqual(Customer.objects.all().count(), 1)

    def get_credentials(self):
        credintails = {
            "email": self.customer_saved.email,
            "password": "qwerty1234",
        }
        return credintails
