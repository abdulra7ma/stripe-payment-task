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
from apps.payment.services.payment import PaymentService


class HomePageView(ListView):
    template_name: str = "items.html"
    queryset = Item.objects.all()
    context_object_name: str = "items"


class ItemView(DetailView):
    template_name: str = "item.html"
    context_object_name: str = "item"

    def get_object(self):
        item_id = self.kwargs.get("item_id")
        item = get_object_or_404(Item, pk=item_id)
        return item


@method_decorator(csrf_exempt, name="dispatch")
class BuyItemView(DetailView):
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


@method_decorator(csrf_exempt, name="dispatch")
class StripeConfig(View):
    def get(self, request, *args, **kwargs) -> JsonResponse:
        stripe_config = {"publicKey": config("STRIPE_PUBLISHABLE_KEY")}
        return JsonResponse(stripe_config, safe=False)


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelledView(TemplateView):
    template_name = "cancelled.html"
