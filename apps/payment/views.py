from typing import Any

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView

from apps.payment.selectors.item import get_item_by_id

from django.http import Http404


class HomePageView(ListView):
    template_name = "home.html"

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        return super().get(request, *args, **kwargs)


class BuyItemView(DetailView):
    pass


class ItemView(DetailView):
    template_name: str = "item.html"
    def get_object(self):
        item_id = self.request.GET.get("item_id")
        item = get_item_by_id(item_id)
        if item:
            return item
        raise Http404


@csrf_exempt
def stripe_config(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
