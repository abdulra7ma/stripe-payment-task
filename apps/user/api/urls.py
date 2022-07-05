# Django imports
from django.urls import path

# app imports
from .views import UserAPIView

urlpatterns = [
    path("", UserAPIView.as_view(), name="user-api"),
    # path("/profile-photo", UserImageAPIView.as_view(), name="profile-photo-api"),
]
