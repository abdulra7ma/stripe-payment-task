# Django imports
from django.urls import path

# app imports
from .views import CustomerAPIView, UserImageAPIView

urlpatterns = [
    path("", CustomerAPIView.as_view(), name="customer-api"),
    path("/profile-photo", UserImageAPIView.as_view(), name="profile-photo-api"),
]
