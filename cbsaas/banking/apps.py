from django.apps import AppConfig


class BankingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cbsaas.banking"

    def ready(self):
        from . import receivers