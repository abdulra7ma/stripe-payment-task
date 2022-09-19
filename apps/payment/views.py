from typing import Any

from decouple import config
from django.http import Http404, HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, TemplateView, View

from apps.payment.models import Item
from apps.payment.selectors.item import get_item_by_id
from apps.payment.services.order import OrderService
from apps.payment.services.payment import PaymentService


class HomePageView(ListView):
    """
    List all the items in the DB
    """

    template_name: str = "items.html"
    queryset = Item.objects.all()
    context_object_name: str = "items"


class ItemView(DetailView):
    """
    View specific Item
    """

    template_name: str = "item.html"
    context_object_name: str = "item"

    def get_object(self):
        item_id = self.kwargs.get("item_id")
        item = get_object_or_404(Item, pk=item_id)
        return item


@method_decorator(csrf_exempt, name="dispatch")
class BuyItemView(DetailView):
    """
    Take an item_id and extract the referenced item from the DB,
    than a request to Stripe and return the result in a JSON format
    """

    def get_object(self):
        item_id = self.kwargs.get("item_id")
        return get_item_by_id(item_id)

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> JsonResponse:
        item = self.get_object()

        if item:
            response = PaymentService().create_payment_intent(item)
            return response

        raise Http404


class CheckoutView(TemplateView):
    template_name: str = "checkout.html"

    def get(self, request, *args, **kwargs):
        """
        Check if item_id in the query parameters exist

        if exist:
            check if item_id has a reference object in the db

            if True:
                Create an Order object
            else:
                raise Http404

        """
        if "item_id" in request.GET:
            # get item_id query parameter from the uri query parameters
            item_id = request.GET.get("item_id")
            item = get_item_by_id(item_id)

            if item:
                # create Order object
                order = OrderService().create_order(item)
            raise Http404

        return super().get(request, *args, **kwargs)


@method_decorator(csrf_exempt, name="dispatch")
class StripeConfig(View):
    """
    Returns the Stripe public key in a JSON format
    """

    def get(self, request, *args, **kwargs) -> JsonResponse:
        stripe_config = {"publicKey": config("STRIPE_PUBLISHABLE_KEY")}
        return JsonResponse(stripe_config, safe=False)


class SuccessView(TemplateView):
    """
    Successful page for Payment success
    """

    template_name = "success.html"


class CancelledView(TemplateView):
    """
    Cancel page for Payment failure
    """

    template_name = "cancelled.html"
