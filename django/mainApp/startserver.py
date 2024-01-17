from django.contrib.auth import get_user_model

def set_all_users_offline():
	# parse all users and set them offline
	# User = get_user_model()
	# for user in User.objects.all():
	# 	user.status = "offline"
	# 	user.save()
    print("set_all_users_offline()")