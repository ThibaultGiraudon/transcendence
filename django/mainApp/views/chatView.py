from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
import uuid

from mainApp.models import Channel


def chat(request):
	if not request.user.is_authenticated:
		return redirect('sign_in')

	# Get the channels
	chats = list(request.user.channels.all())
	
	return render(request, "chat/chat.html", { 'chats': chats })


def create_channel(request):
	if not request.user.is_authenticated:
		return redirect('sign_in')
	
	# Get the ids
	ids = []
	for id in request.GET.getlist('id'):
		try:
			ids.append(int(id))
		except ValueError:
			continue

	# Create a default channel name
	if (len(ids) == 2):
		channel_name = "private channel"
	else:
		channel_name = "group channel"
	
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
		return redirect('chat')
	
	# Adapt the channel name
	elif len(users) == 2:
		for user in users:
			if user.id != request.user.id:
				channel_name = user.username + " & " + request.user.username
				break

	# Create the channel
	channel = Channel.objects.create(name=channel_name, room_name=room_name)
	channel.users.set(users)
	channel.save()

	return redirect('room', room_name=room_name)


def room(request, room_name):
	if not request.user.is_authenticated:
		return redirect('sign_in')

	# Get the channel
	try:
		channel = Channel.objects.get(room_name=room_name)
	except Channel.DoesNotExist:
		return redirect('chat')
	
	# Get the users in the channel
	users = list(channel.users.all())
	
	# Get the blocked users
	blocked_users = request.user.blockedUsers

	# Update the status of the current user
	request.user.status = f"chat:{room_name}"
	request.user.save()
 
	return render(request, "chat/room.html", {"room_name": room_name, "blocked_users": blocked_users, "users": users})