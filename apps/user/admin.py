# Django imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.sites.models import Site

# app imports
from .models import User, UserPic

admin.site.unregister(Site)


class SiteAdmin(admin.ModelAdmin):
    fields = ("id", "name", "domain")
    readonly_fields = ("id",)
    list_display = ("id", "name", "domain")
    list_display_links = ("name",)
    search_fields = ("name", "domain")


admin.site.register(Site, SiteAdmin)


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "id",
        "email",
        "first_name",
        "surname",
        "is_active",
        "is_frozen",
    )
    list_filter = (
        "email",
        "is_frozen",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "first_name",
                    "middle_name",
                    "phone_number",
                    "birthday",
                    "city",
                    "surname",
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_frozen",
                    "is_active",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "middle_name",
                    "phone_number",
                    "birthday",
                    "city",
                    "surname",
                    "password1",
                    "password2",
                    "is_frozen",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserPic)
