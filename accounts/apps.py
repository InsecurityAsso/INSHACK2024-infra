from django.apps import AppConfig

from .tasks import TokenCleaner, FileCleaner


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        TokenCleaner()
        FileCleaner()

