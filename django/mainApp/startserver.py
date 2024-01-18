from django.contrib.auth import get_user_model

def set_all_users_offline():
	try:
		User = get_user_model()
		for user in User.objects.all():
			user.status = "offline"
			user.save()
	except:
		pass