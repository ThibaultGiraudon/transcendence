from django.apps import AppConfig

class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainApp'
    def ready(self):
        from . import startserver
        startserver.set_all_users_offline()
