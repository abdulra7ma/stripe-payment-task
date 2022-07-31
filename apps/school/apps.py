# Django imports
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "school"

    def ready(self) -> None:
        import school.signals
