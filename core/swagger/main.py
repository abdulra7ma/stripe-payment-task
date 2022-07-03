# Django imports
from django.urls import include, path, re_path

# external imports
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Define Swagger API Schema
schema_view = get_schema_view(
    openapi.Info(
        title="ISAY FLY API",
        default_version="v1",
        description="",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


