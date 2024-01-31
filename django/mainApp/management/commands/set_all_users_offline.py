from django.core.management.base import BaseCommand
from mainApp import startserver

class Command(BaseCommand):
	help = 'Set all users offline'

	def handle(self, *args, **options):
		startserver.set_all_users_offline()