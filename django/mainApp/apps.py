from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from django.apps import AppConfig


class MainAppConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'mainApp'
	
	def ready(self):
		import mainApp.signals

		post_migrate.connect(launch_set_users_offline, sender=self)


@receiver(post_migrate)
def launch_set_users_offline(sender, **kwargs):
	from .utils import set_all_users_offline
	try:
		set_all_users_offline()
	except:
		pass