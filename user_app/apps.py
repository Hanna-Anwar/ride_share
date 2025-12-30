from django.apps import AppConfig


class UserAppConfig(AppConfig):
    name = 'user_app'

# to activate signal

    def ready(self):
        import user_app.signals