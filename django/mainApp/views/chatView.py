from django.contrib.auth import get_user_model
import uuid

from mainApp.models import Channel
from mainApp.views.utils import renderPage, redirectPage


def chat(request):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')

	# Get the channels
	channels = list(request.user.channels.all())

	# Get the channels names
	chats = []
	for i in range(len(channels)):
		users = list(channels[i].users.all())
		if channels[i].private and len(users) == 2:
			if users[0].id == request.user.id:
				if users[1].id in request.user.blockedUsers:
					continue
				chats.append([channels[i], users[1].username])
			else:
				if users[0].id in request.user.blockedUsers:
					continue
				chats.append([channels[i], users[0].username])
		else:
			chats.append([channels[i], channels[i].name])
	
	return renderPage(request, 'chat/chat.html', { 'chats': chats })


def create_channel(request):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')
	
	# Get parameters
	private = request.GET.get('private', 'False') == 'True'
	try:
		user_ids = list(map(int, request.GET.getlist('user_ids')))
	except ValueError:
		return redirectPage(request, '/chat/')

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
			return redirectPage(request, '/chat/')
	
	# Check if the channel is empty
	if len(users) == 0:
		return redirectPage(request, '/chat/')
	
	# Check if the channel is really private
	if private and len(users) != 2:
		return redirectPage(request, '/chat/')
	
	# Check if a private channel already exists between the two users
	if len(users) == 2:
		existing_channel = Channel.objects.filter(users__in=user_ids, private=True)
		if existing_channel.exists():
			return redirectPage(request, '/chat/' + existing_channel.first().room_id)

	# Create the channel
	channel = Channel.objects.create(private=private, room_id=room_id, name=channel_name)
	channel.users.set(users)
	channel.save()

	return redirectPage(request, '/chat/' + room_id)


def room(request, room_id):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')

	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>", room_id)

	# Get the channel
	try:
		channel = Channel.objects.get(room_id=room_id)
	except Channel.DoesNotExist:
		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> bordel de queue")
		return redirectPage(request, '/chat/')
	
	# Get the users in the channel
	users = list(channel.users.all())
	
	# Get the blocked users
	blocked_users = request.user.blockedUsers

	# Check if the channel is private and the other user is blocked
	if channel.private and len(users) == 2:
		if users[0].id == request.user.id:
			if users[1].id in blocked_users:
				return redirectPage(request, '/chat/')
		else:
			if users[0].id in blocked_users:
				return redirectPage(request, '/chat/')

	# Update the status of the current user
	request.user.status = f"chat:{room_id}"
	request.user.save()

	# Sort messages by timestamp
	messages = channel.messages
	messages.sort(key=lambda x: x['timestamp'])

	# Get the name and the photo of the channel
	if channel.private and len(users) == 2:
		if users[0].id == request.user.id:
			name_channel = users[1].username
			photo_channel = users[1].photo
		else:
			name_channel = users[0].username
			photo_channel = users[0].photo
	else:
		name_channel = channel.name
		photo_channel = None

	# Change blocked users to a list of string for the template
	blocked_users_str = ""
	for blocked_user in blocked_users:
		blocked_users_str += str(blocked_user) + ","
 
	# Context
	context = {
		'messages': messages,
		'users': users,
		'name_channel': name_channel,
		'photo_channel': photo_channel,
		'room_id': room_id,
		'blocked_users': blocked_users,
		'blocked_users_str': blocked_users_str,
		'private': channel.private,
	}

	return renderPage(request, 'chat/room.html', context)