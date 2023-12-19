from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
import uuid

def chat(request):
	if not request.user.is_authenticated:
		return redirect('sign_in')
	
	User = get_user_model()
	users = User.objects.all()

	chats = []

	for id, value in request.user.channels.items():
		for user in users:
			if user.id == int(id):
				chats.append({'user': user, 'link': value})

	return render(request, "chat/chat.html", { 'chats': chats })

def create_channel(request, id):
	if not request.user.is_authenticated:
		return redirect('sign_in')
	
	room_name = str(uuid.uuid1())
	
	User = get_user_model()
	try:
		user_to = User.objects.get(id=id)
	except User.DoesNotExist:
		return redirect('users')

	request.user.channels.update({user_to.id: room_name})
	request.user.save()

	user_to.channels.update({request.user.id: room_name})
	user_to.save()

	return redirect('room', room_name=room_name)

def room(request, room_name):
	if not request.user.is_authenticated:
		return redirect('sign_in')
	
	user_to = None
	for id, channel in request.user.channels.items():
		if channel == room_name:
			user_to = get_user_model().objects.get(id=int(id))
			break

	if user_to is None:
		return redirect('chat')

	request.user.status = f"chat:{user_to.id}"
	request.user.save()
 
	return render(request, "chat/room.html", {"room_name": room_name, "user_to": user_to})