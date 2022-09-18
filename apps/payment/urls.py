from django.urls import path

from .views import BuyItemView, HomePageView, ItemView

urlpatterns = [
    path("", HomePageView.as_view(), name="home_page"),
    path("/item/<int:item_id>", ItemView.as_view(), name="item"),
    path("/buy/<int:item_id>", BuyItemView.as_view(), name="buy-item"),
]
