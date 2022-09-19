import stripe
from decouple import config
from django.http.response import JsonResponse

from apps.payment.models import Item


class PaymentService:
    def create_checkout_session(
        self, item: Item, currency: str = "usd"
    ) -> JsonResponse:
        """
        Create new Checkout Session for the order

        :param Item item: Item object to make payment out of it
        :param str currency: currency code for stripe payment

        :return: sessionId for stripe order or error
        :rtype: Item or None

        """
        domain_url = "http://localhost:8000/"
        stripe.api_key = config("STRIPE_SECRET_KEY", cast=str)
        try:
            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url
                + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancelled/",
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        "quantity": 1,
                        "price_data": {
                            "product_data": {
                                "name": item.name,
                                "description": item.description,
                            },
                            "unit_amount": self.safe_dollar_to_cent(
                                item.price
                            ),
                            "currency": currency,
                        },
                    }
                ],
            )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})

    def create_payment_intent(self, item: Item, currency: str = "usd"):
        stripe.api_key = config("STRIPE_SECRET_KEY", cast=str)

        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=self.safe_dollar_to_cent(item.price),
                currency=currency,
                payment_method_types=["card"],
            )
            return JsonResponse(payment_intent)
        except Exception as e:
            print(str(e))
            return JsonResponse({"error": str(e)})

    def safe_dollar_to_cent(self, dollar_amount: float | int) -> int:
        """
        Convert dollar to cent

        :param float dollar_amount: dollar amount to be converted to cents

        :return: converted dollor amount in cents
        :rtype: int

        """
        cents = float(dollar_amount) * 100
        return int(cents)
