from django.urls import path

from .views import LoginView, SignupView
from django.contrib.auth import views as auth_views

app_name = 'auth'

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/auth/login/"), name="logout"),
]
