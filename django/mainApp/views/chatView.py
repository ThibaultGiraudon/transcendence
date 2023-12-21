from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
import uuid
from django.http import JsonResponse

from mainApp.models import Channel
from mainApp.views.utils import renderPage


def chat(request):
	if not request.user.is_authenticated:
		return JsonResponse({'redirect': '/sign_in/'})

	# Get the channels
	chats = list(request.user.channels.all())
	
	return renderPage(request, 'chat/chat.html', { 'chats': chats })


def create_channel(request, ids):
	if not request.user.is_authenticated:
		return JsonResponse({'redirect': '/sign_in/'})
	
	# Get the ids
	ids = [int(id) for id in ids.split(',')]

	# Create a default channel name
	channel_name = "group"
	other_name = ""
	
	# Channel informations
	room_name = str(uuid.uuid1())
	users = []

	# Get the users
	User = get_user_model()
	for id in ids:
		try:
			user = User.objects.get(id=id)
		except User.DoesNotExist:
			continue
		users.append(user)
	
	# Check if the channel is empty
	if len(users) == 0:
		return JsonResponse({'redirect': '/chat/'})
	
	# Adapt the channel name
	elif len(users) == 2:
		for user in users:
			if user.id != request.user.id:
				channel_name = user.username
			else:
				other_name = request.user.username
				break

	# Create the channel
	channel = Channel.objects.create(name=channel_name, room_name=room_name, other_name=other_name)
	channel.users.set(users)
	channel.save()

	return JsonResponse({'redirect': '/chat/room/' + room_name + '/'})


def room(request, room_name):
	if not request.user.is_authenticated:
		return JsonResponse({'redirect': '/sign_in/'})

	# Get the channel
	try:
		channel = Channel.objects.get(room_name=room_name)
	except Channel.DoesNotExist:
		return JsonResponse({'redirect': '/chat/'})
	
	# Get the users in the channel
	users = list(channel.users.all())
	
	# Get the blocked users
	blocked_users = request.user.blockedUsers

	# Update the status of the current user
	request.user.status = f"chat:{room_name}"
	request.user.save()
 
	# Context
	context = {
		'room_name': room_name,
		'users': users,
		'blocked_users': blocked_users,
	}
	
	return renderPage(request, 'chat/room.html', context)