from django.contrib import admin

from apps.payment.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "price",
    )
