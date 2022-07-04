# Django imports
from django.urls import path

# app imports
from .views import UserAPIView, UserImageAPIView

urlpatterns = [
    path("", UserAPIView.as_view(), name="user-api-1"),
    # path("/profile-photo", UserImageAPIView.as_view(), name="profile-photo-api"), 
]
