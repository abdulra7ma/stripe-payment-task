# Django imports
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user"

    def ready(self) -> None:
        # return super().ready()
        import user.signals
