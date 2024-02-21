from django.apps import AppConfig

class MainAppConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'mainApp'
	
	def ready(self):
		from .utils import set_all_users_offline
		import mainApp.signals
		set_all_users_offline()