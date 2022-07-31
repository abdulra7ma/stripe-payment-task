from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "admin/doc/",
        include("django.contrib.admindocs.urls"),
    ),
    path(
        "school/",
        include("school.urls", namespace="school"),
    ),
    path(
        "auth/",
        include("authentication.urls"),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
