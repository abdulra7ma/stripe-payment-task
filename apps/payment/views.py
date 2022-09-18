from typing import Any, Optional

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.http.response import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from django.views.generic import ListView, TemplateView, DetailView



class HomePageView(ListView):
    template_name = "home.html"

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        return super().get(request, *args, **kwargs)


class BuyItemView(DetailView):
    pass

class ItemView(DetailView):
    def get_object(self):
        return 


@csrf_exempt
def stripe_config(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
