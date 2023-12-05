from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
import uuid

def chat(request):
	if not request.user.is_authenticated:
		return redirect('sign_in')
	
	users = get_user_model().objects.all()

	return render(request, "chat/chat.html", {'channels': request.user.channels, 'users': users})


def create_channel(request, user_to):
	if not request.user.is_authenticated:
		return redirect('sign_in')
	
	room_name = str(uuid.uuid1())
	
	try:
		user_to = get_user_model().objects.get(username=user_to)
	except get_user_model().DoesNotExist:
		return redirect('users')

	request.user.channels.update({user_to.get_username(): room_name})
	request.user.save()

	user_to.channels.update({request.user.get_username(): room_name})
	user_to.save()

	return redirect('room', room_name=room_name)


def room(request, room_name):
	if not request.user.is_authenticated:
		return redirect('sign_in')
	
	return render(request, "chat/room.html", {"room_name": room_name})