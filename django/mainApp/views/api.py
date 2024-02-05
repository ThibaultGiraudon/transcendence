from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model, logout
from django.middleware.csrf import get_token
from django.utils import timezone
import uuid

from ..models import Notification, Channel


def get_username(request, id):
	if not request.user.is_authenticated:
		return JsonResponse({'username': None}, status=401)

	# Check if the user exist
	User = get_user_model()
	try:
		user = User.objects.get(id=id)
	except User.DoesNotExist:
		return JsonResponse({'username': None}, status=401)
	
	return JsonResponse({'username': user.username}, status=200)


def sign_out(request):
	if request.user.is_authenticated:
		# Sign out the user
		request.user.set_status("offline")
		logout(request)

		return JsonResponse({'success': True, "message": "Successful sign out"}, status=200)
	else:
		return JsonResponse({'success': False, "message": "The user is not authenticated"}, status=401)


def isAuthenticated(request):
	if request.user.is_authenticated:
		return JsonResponse({'isAuthenticated': True}, status=200)
	else:
		return JsonResponse({'isAuthenticated': False}, status=401)


def header(request):
	if not request.user.is_authenticated:
		return JsonResponse({
			'isAuthenticated': False,
		},
		status=401)
	
	return JsonResponse({
		'isAuthenticated': request.user.is_authenticated,
		'username': request.user.username,
		'photo_url': request.user.photo.url,
		'nbNewNotifications': request.user.nbNewNotifications,
	},
	status=200)
	

def get_user(request, username=None):
	if not request.user.is_authenticated:
		return JsonResponse({'user': None, 'isCurrentUser': False, 'isAuthenticated': False}, status=401)

	# Get informations about the current user
	if not username or username == request.user.username or username == "me":
		channels_dict = {}
		channels = list(request.user.channels.all())
		for channel in channels:

			# Get users
			users_dict = {}
			for user in channel.users.all():
				users_dict[user.id] = {
					'id': user.id,
					'username': user.username,
					'photo_url': user.photo.url,
					'status': user.status,
					'followed': user.id in request.user.follows,
					'blocked': user.id in request.user.blockedUsers,
				}

			# Get last message of the channel
			last_message_obj = channel.messages.order_by('-timestamp').first()
			if last_message_obj:
				sender = last_message_obj.sender.id
				if sender == request.user.id:
					sender = request.user.username
				else:
					for user in channel.users.all():
						if user.id == int(sender):
							sender = user.username
							break

				last_message = {
					'sender': "You" if sender == request.user.username else sender,
					'message': last_message_obj.message if not last_message_obj.sender.id in request.user.blockedUsers else "This message is blocked",
					'timestamp': timezone.localtime(last_message_obj.timestamp).strftime("%d-%m-%Y %H:%M"),
				}
			else:
				last_message = None

			# Change the name of the channel if it is a private channel
			if channel.private and len(channel.users.all()) == 2:
				for user in channel.users.all():
					if user.id != request.user.id:
						channel_name = user.username
						break
			else:
				channel_name = channel.name

			# Add channel to the list
			channels_dict[channel.room_id] = {
				'id': channel.id,
				'room_id': channel.room_id,
				'name': channel_name,
				'private': channel.private,
				'users': users_dict,
				'last_message': last_message,
			}

		# Get informations about the user
		user_dict = {
			'id': request.user.id,
			'email': request.user.email,
			'username': request.user.username,
			'photo_url': request.user.photo.url,
			'status': request.user.status,
			'nbNewNotifications': request.user.nbNewNotifications,
			'channels': channels_dict,
			'follows': request.user.follows,
			'blockedUsers': request.user.blockedUsers,
		}
		return JsonResponse({'user': user_dict, 'isCurrentUser': True, 'isAuthenticated': True}, status=200)
	
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
			'followed': user.id in request.user.follows,
			'blocked': user.id in request.user.blockedUsers,
		}
		return JsonResponse({'user': user_dict, 'isCurrentUser': False}, status=200)


def users(request):
	if not request.user.is_authenticated:
		return JsonResponse({'users': None}, status=401)

	# Get all users
	User = get_user_model()
	users = list(User.objects.all())
	users_dict = {}
	for user in users:
		if user.id == request.user.id:
			continue
		
		users_dict[user.id] = {
			'id': user.id,
			'username': user.username,
			'photo_url': user.photo.url,
			'status': user.status,
			'followed': user.id in request.user.follows,
			'blocked': user.id in request.user.blockedUsers,
		}

	return JsonResponse({'users': users_dict}, status=200)


def follow(request, id):
	if not request.user.is_authenticated:
		return JsonResponse({'success': False, "message": "The user is not authenticated"}, status=401)

	# Convert ID
	try:
		id = int(id)
	except ValueError:
		return JsonResponse({'success': False, "message": "Invalid id"}, status=401)

	# Check if the user exist and if he is not already followed
	User = get_user_model()
	try:
		userTo = User.objects.get(id=id)
		if id in request.user.follows:
			return JsonResponse({'success': False, "message": "User already blocked"}, status=401)
	except User.DoesNotExist:
		return JsonResponse({'success': False, "message": "User does not exist"}, status=401)
	
	notification = Notification(user=userTo, message=f"{request.user.username} is now following you.")
	notification.save()
 
	request.user.follows.append(id)
	request.user.save()
	
	return JsonResponse({'success': True, "message": "Successful follow"}, status=200)


def unfollow(request, id):
	if not request.user.is_authenticated:
		return JsonResponse({'success': False, "message": "The user is not authenticated"}, status=401)
	
	# Convert ID
	try:
		id = int(id)
	except ValueError:
		return JsonResponse({'success': False, "message": "Invalid id"}, status=401)
	
	# Check if the user exist and if he is followed
	User = get_user_model()
	try:
		userTo = User.objects.get(id=id)
		if id not in request.user.follows:
			return JsonResponse({'success': False, "message": "User already blocked"}, status=401)
	except User.DoesNotExist:
		return JsonResponse({'success': False, "message": "User does not exist"}, status=401)

	request.user.follows.remove(id)
	request.user.save()

	return JsonResponse({'success': True, "message": "Successful unfollow"}, status=200)


def block(request, id):
	if not request.user.is_authenticated:
		return JsonResponse({'success': False, "message": "The user is not authenticated"}, status=401)
	
	# Convert ID
	try:
		id = int(id)
	except ValueError:
		return JsonResponse({'success': False, "message": "Invalid id"}, status=401)

	# Check if the user exist and if he is not already blocked
	User = get_user_model()
	try:
		userTo = User.objects.get(id=id)
		if id in request.user.blockedUsers:
			return JsonResponse({'success': False, "message": "User already blocked"}, status=401)
	except User.DoesNotExist:
		return JsonResponse({'success': False, "message": "User does not exist"}, status=401)
	
	# Unfollow the user if he is in the follows list
	if id in request.user.follows:
		request.user.follows.remove(id)
 
	# Block the user
	request.user.blockedUsers.append(id)
	request.user.save()

	return JsonResponse({'success': True, "message": "Successful block"}, status=200)


def unblock(request, id):
	if not request.user.is_authenticated:
		return JsonResponse({'success': False, "message": "The user is not authenticated"}, status=401)
	
	# Convert ID
	try:
		id = int(id)
	except ValueError:
		return JsonResponse({'success': False, "message": "Invalid id"}, status=401)
	
	# Check if the user exist and if he is blocked
	User = get_user_model()
	try:
		userTo = User.objects.get(id=id)
		if id not in request.user.blockedUsers:
			return JsonResponse({'success': False, "message": "User already blocked"}, status=401)
	except User.DoesNotExist:
		return JsonResponse({'success': False, "message": "User does not exist"}, status=401)

	# Unblock the user
	request.user.blockedUsers.remove(id)
	request.user.save()

	return JsonResponse({'success': True, "message": "Successful unblock"}, status=200)


def get_notifications(request):
	if not request.user.is_authenticated:
		return JsonResponse({'notifications': None}, status=401)

	# Get notifications
	notifications = list(request.user.notifications.all().order_by('-date'))
	request.user.nbNewNotifications = 0
	request.user.save()
	
	notifications_dict = {}
	for notification in notifications:
		notifications_dict[notification.id] = {
			'id': notification.id,
			'message': notification.message,
			'date': timezone.localtime(notification.date).strftime("%d-%m-%Y %H:%M"),
			'read': notification.read,
		}
	
	# Mark all notifications as read
	request.user.notifications.all().update(read=True)
	
	return JsonResponse({'notifications': notifications_dict}, status=200)


def delete_notification(request, id):
	if not request.user.is_authenticated:
		return JsonResponse({'success': False, "message": "The user is not authenticated"}, status=401)

	# Get notification
	try:
		notification = request.user.notifications.get(id=id)
	except ObjectDoesNotExist:
		return JsonResponse({'success': False, "message": "Notification does not exist"}, status=401)

	# Delete notification
	notification.delete()

	return JsonResponse({'success': True, "message": "Notification deleted"}, status=200)


def delete_all_notifications(request):
	if not request.user.is_authenticated:
		return JsonResponse({'success': False, "message": "The user is not authenticated"}, status=401)

	# Delete all notifications
	request.user.notifications.all().delete()

	return JsonResponse({'success': True, "message": "All notifications deleted"}, status=200)


def get_messages(request, room_id):
	if not request.user.is_authenticated:
		return JsonResponse({'messages': None}, status=401)

	# Get channel
	try:
		channel = request.user.channels.get(room_id=room_id)
	except ObjectDoesNotExist:
		return JsonResponse({'messages': None}, status=401)
	
	# Get messages
	messages = channel.messages.all().order_by('timestamp')
	messages_dict = {}
	
	for message in messages:
		messages_dict[message.id] = {
			'sender': message.sender.id,
			'username': message.sender.username,
			'message': message.message,
			'timestamp': message.timestamp,
		}
	
	return JsonResponse({'messages': messages_dict}, status=200)


def create_channel(request):
	if not request.user.is_authenticated:
		return JsonResponse({'success': False, 'message': 'The user is not authenticated'}, status=401)
	
	# Get parameters
	private = request.GET.get('private', 'False') == 'True'
	try:
		user_ids = list(map(int, request.GET.getlist('user_ids')))
	except ValueError:
		return JsonResponse({'success': False, 'message': 'Invalid user_ids'}, status=401)

	# Create a default channel name
	channel_name = "group"
	
	# Channel informations
	room_id = str(uuid.uuid1())
	users = []

	# Get the users
	User = get_user_model()
	for user_id in user_ids:
		try:
			user = User.objects.get(id=user_id)
			users.append(user)
		except User.DoesNotExist:
			return JsonResponse({'success': False, 'message': f"User {user_id} does not exist"}, status=401)
	
	# Check if the channel is empty
	if len(users) == 0:
		return JsonResponse({'success': False, 'message': 'The channel is empty'}, status=401)
	
	# Check if the channel is really private
	if private and len(users) != 2:
		return JsonResponse({'success': False, 'message': 'A private channel must have exactly two users'}, status=401)
	
	# Check if a private channel already exists between the two users
	if len(users) == 2:
		existing_channel = Channel.objects.filter(private=True, users=users[0]).filter(users=users[1])
		if existing_channel.exists():
			return JsonResponse({'success': False, 'message': 'A private channel already exists between the two users'}, status=401)

	# Create the channel
	channel = Channel.objects.create(private=private, room_id=room_id, name=channel_name)
	channel.users.set(users)
	channel.save()

	return JsonResponse({'success': True, 'message': 'Channel created', 'room_id': room_id}, status=200)


def generate_csrf_token(request):
	csrf_token = get_token(request)
	return JsonResponse({'token': csrf_token}, status=200)


def get_game_info(request):
	if not request.user.is_authenticated:
		return JsonResponse({'success': False, 'game_id': None, 'player_id': None}, status=401)

	return JsonResponse({'success': True, 'game_id': request.user.player.currentGameID, 'player_id': request.user.player.id}, status=200)