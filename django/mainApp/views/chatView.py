from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core import serializers
import uuid
from django.http import JsonResponse

from mainApp.models import CustomUser
from mainApp.models import Channel
from mainApp.views.utils import renderPage


def chat(request):
	if not request.user.is_authenticated:
		return JsonResponse({'redirect': '/sign_in/'})

	# Get the channels
	channels = list(request.user.channels.all())

	# Get the channels names
	chats = []
	for i in range(len(channels)):
		users = list(channels[i].users.all())
		if channels[i].private and len(users) == 2:
			if users[0].id == request.user.id:
				chats.append([channels[i], users[1].username])
			else:
				chats.append([channels[i], users[0].username])
		else:
			chats.append([channels[i], channels[i].name])
	
	return renderPage(request, 'chat/chat.html', { 'chats': chats })


def create_channel(request):
	if not request.user.is_authenticated:
		return JsonResponse({'redirect': '/sign_in/'})
	
	# Get parameters
	private = request.GET.get('private', 'False') == 'True'
	try:
		user_ids = list(map(int, request.GET.getlist('user_ids')))
	except ValueError:
		return JsonResponse({'redirect': '/chat/'})

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
			return JsonResponse({'redirect': '/chat/'})
	
	# Check if the channel is empty
	if len(users) == 0:
		return JsonResponse({'redirect': '/chat/'})
	
	# Check if the channel is really private
	if private and len(users) != 2:
		return JsonResponse({'redirect': '/chat/'})
	
	# Check if a private channel already exists between the two users
	if len(users) == 2:
		existing_channel = Channel.objects.filter(users__in=user_ids, private=True)
		if existing_channel.exists():
			return JsonResponse({'redirect': '/chat/' + existing_channel.first().room_id})

	# Create the channel
	channel = Channel.objects.create(private=private, room_id=room_id, name=channel_name)
	channel.users.set(users)
	channel.save()

	return JsonResponse({'redirect': '/chat/' + room_id})


def room(request, room_id):
	if not request.user.is_authenticated:
		return JsonResponse({'redirect': '/sign_in/'})

	# Get the channel
	try:
		channel = Channel.objects.get(room_id=room_id)
	except Channel.DoesNotExist:
		return JsonResponse({'redirect': '/chat/'})
	
	# Get the users in the channel
	users = list(channel.users.all())
	
	# Get the blocked users
	blocked_users = request.user.blockedUsers

	# Update the status of the current user
	request.user.status = f"chat:{room_id}"
	request.user.save()
 
	# Context
	context = {
		'name_channel': channel.name,
		'room_id': room_id,
		'users': users,
		'blocked_users': blocked_users,
		'private': channel.private,
	}

	return renderPage(request, 'chat/room.html', context)


def get_message_history(request, room_id):
	print(">>>>>>>>>>>>>>>>>>get_message_history(", room_id, ")")
	
	try:
		channel = Channel.objects.get(room_id=room_id)
		messages = channel.messages
	except Channel.DoesNotExist:
		messages = []

	return JsonResponse(messages, safe=False)