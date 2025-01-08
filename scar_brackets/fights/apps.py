from django.apps import AppConfig


class FightConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "fights"


class MyAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "fights"

    def ready(self):
        import fights.signals  # Import the signals module
