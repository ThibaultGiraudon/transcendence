from django.http import JsonResponse
from django.contrib.auth import get_user_model, logout


def api_get_username(request, id):
	if not request.user.is_authenticated:
		return JsonResponse({'username': None})

	# Check if the user exist
	User = get_user_model()
	try:
		user = User.objects.get(id=id)
	except User.DoesNotExist:
		return JsonResponse({'username': None})
	
	return JsonResponse({'username': user.username})


def api_sign_out(request):
	if request.user.is_authenticated:
		# Sign out the user
		request.user.set_status("offline")
		logout(request)

		return JsonResponse({'success': True, "message": "Successful sign out"})
	else:
		return JsonResponse({'success': False, "message": "The user is not authenticated"})


def api_is_authenticated(request):
	if request.user.is_authenticated:
		return JsonResponse({'isAuthenticated': True})
	else:
		return JsonResponse({'isAuthenticated': False})
	

def api_get_user(request, username=None):
	if not request.user.is_authenticated:
		return JsonResponse({'user': None, 'isCurrentUser': False})

	# Get informations about the current user
	if not username or username == request.user.username or username == "me":
		channels_dict = {}
		channels = list(request.user.channels.all())
		for channel in channels:

			users_dict = {}
			for user in channel.users.all():
				users_dict[user.id] = {
					'id': user.id,
					'username': user.username,
					'photo_url': user.photo.url,
					'status': user.status,
				}

			channels_dict[channel.room_id] = {
				'id': channel.id,
				'name': channel.name,
				'private': channel.private,
				'users': users_dict,
			}

		user_dict = {
			'id': request.user.id,
			'email': request.user.email,
			'username': request.user.username,
			'photo_url': request.user.photo.url,
			'follows': request.user.follows,
			'status': request.user.status,
			'nbNewNotifications': request.user.nbNewNotifications,
			'blockedUsers': request.user.blockedUsers,
			'channels': channels_dict,
		}
		return JsonResponse({'user': user_dict, 'isCurrentUser': True})
	
	# Get informations about the user with the username
	else:
		User = get_user_model()
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			return JsonResponse({'user': None})
		
		user_dict = {
			'id': user.id,
			'username': user.username,
			'photo_url': user.photo.url,
			'status': user.status,
		}
		return JsonResponse({'user': user_dict, 'isCurrentUser': False})


def api_users(request):
	if not request.user.is_authenticated:
		return JsonResponse({'users': None})

	# Get all users
	User = get_user_model()
	users = list(User.objects.all())
	users_dict = {}
	for user in users:
		users_dict[user.id] = {
			'id': user.id,
			'username': user.username,
			'photo_url': user.photo.url,
			'status': user.status,
		}

	return JsonResponse({'users': users_dict})


def api_follows(request):
	if not request.user.is_authenticated:
		return JsonResponse({'follows': None})

	# Get all follows
	followsIDs = request.user.follows
	follows_dict = {}

	for followID in followsIDs:

		# Get the user
		User = get_user_model()
		try:
			followUser = User.objects.get(id=followID)
		except User.DoesNotExist:
			continue

		# Add the user to the follows
		follows_dict[followUser.id] = {
			'id': followUser.id,
			'username': followUser.username,
			'photo_url': followUser.photo.url,
			'status': followUser.status,
		}

	return JsonResponse({'follows': follows_dict})