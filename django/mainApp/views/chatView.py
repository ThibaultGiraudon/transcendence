from django.contrib.auth import get_user_model
import uuid, logging

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
		
		# Get the username of the sender
		sender = channels[i].messages[-1]['sender']
		if sender == request.user.id:
			sender = request.user.username
		else:
			for user in users:
				if user.id == int(sender):
					sender = user.username
					break

		last_message = {
			'sender': sender,
			'message': channels[i].messages[-1]['message'],
			'timestamp': channels[i].messages[-1]['timestamp'],
		}
		
		if channels[i].private and len(users) == 2:
			if users[0].id == request.user.id:
				if users[1].id in request.user.blockedUsers:
					continue
				chats.append([channels[i], users[1].username, last_message])
			else:
				if users[0].id in request.user.blockedUsers:
					continue
				chats.append([channels[i], users[0].username, last_message])
		else:
			chats.append([channels[i], channels[i].name, last_message])
	
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
			logging.info(f"User {user.username} added to the channel")
		except User.DoesNotExist:
			logging.info(f"User {user_id} does not exist")
			return redirectPage(request, '/chat/')
	
	# Check if the channel is empty
	if len(users) == 0:
		logging.info("No user in the channel")
		return redirectPage(request, '/chat/')
	
	# Check if the channel is really private
	if private and len(users) != 2:
		logging.info("Private channel with more than 2 users")
		return redirectPage(request, '/chat/')
	
	# Check if a private channel already exists between the two users
	if len(users) == 2:
		# check if users[0] and users[1] have a private channel
		existing_channel = Channel.objects.filter(private=True, users=users[0]).filter(users=users[1])
		if existing_channel.exists():
			logging.info("Private channel already exists")
			return redirectPage(request, '/chat/' + existing_channel.first().room_id)

	# Create the channel
	channel = Channel.objects.create(private=private, room_id=room_id, name=channel_name)
	channel.users.set(users)
	channel.save()

	return redirectPage(request, '/chat/' + room_id)


def room(request, room_id):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')

	# Get the channel
	try:
		channel = Channel.objects.get(room_id=room_id)
	except Channel.DoesNotExist:
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

	return renderPage(request, 'chat/room.html', context, userStatus=f"chat:{room_id}")