# Django imports
from django.urls import include, path, re_path

# app imports
from .main import schema_view

swagger_urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema_json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui(
            "swagger",
            cache_timeout=0,
        ),
        name="schema_swagger_ui",
    ),
    re_path(
        r"^redoc/$",
        schema_view.with_ui(
            "redoc",
            cache_timeout=0,
        ),
        name="schema_redoc",
    ),
]
