# Django imports
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

# external imports
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# app imports
from .swagger.urls import swagger_urlpatterns

# include all your api endpoints here
api_urlpatterns = []

# include any token related endpoint
token_urlpatterns = [
    path(
        "token",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "token/verify",
        TokenVerifyView.as_view(),
        name="token_verify",
    ),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "admin/doc/",
        include("django.contrib.admindocs.urls"),
    ),
    path("api/v1/self-service/", include(api_urlpatterns + token_urlpatterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# activate swagger urls
urlpatterns += swagger_urlpatterns
