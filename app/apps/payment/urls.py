from django.urls import path

from .views import (BuyItemView, CancelledView, CheckoutView, HomePageView,
                    ItemView, StripeConfig, SuccessView)

urlpatterns = [
    path("", HomePageView.as_view(), name="home-page"),
    path("item/<int:item_id>", ItemView.as_view(), name="item"),
    path("buy/<int:item_id>", BuyItemView.as_view(), name="buy-item"),
    path("checkout", CheckoutView.as_view(), name="checkout"),
    path("success", SuccessView.as_view(), name="payment-success"),
    path("cancelled", CancelledView.as_view(), name="payment-cancel"),
    path("config", StripeConfig.as_view(), name="payment-config"),
]
