import uuid, json
from django.shortcuts import render
from django.http import JsonResponse

from mainApp.models import Channel
from mainApp.utils import containBadwords


def chat(request):
	if request.method == 'GET':
		return render(request, 'base.html')


def new(request):
	if request.method == 'GET':
		return render(request, 'base.html')

	elif request.method == 'POST':
		if not request.user.is_authenticated:
			return JsonResponse({'success': False, 'message': 'The user is not authenticated'}, status=401)

		# Get parameters
		data = json.loads(request.body)
		name = data.get('name')
		description = data.get('description')

		# Check name
		if not name:
			return JsonResponse({'success': False, 'name': 'The name is required'}, status=401)
		elif len(name) > 30:
			return JsonResponse({'success': False, 'name': 'The name is too long'}, status=401)
		elif name.isspace():
			return JsonResponse({'success': False, 'name': 'The name cannot be only white spaces'}, status=401)
		elif containBadwords(name):
			return JsonResponse({'success': False, 'name': 'The name contains bad words'}, status=401)

		# Check description
		if not description:
			description = ''
		elif len(description) > 150:
			return JsonResponse({'success': False, 'description': 'The description is too long'}, status=401)
		elif containBadwords(description):
			return JsonResponse({'success': False, 'description': 'The description contains bad words'}, status=401)

		# Channel informations
		room_id = str(uuid.uuid4())
		users = [request.user.id]

		# Create the chat group
		channel = Channel.objects.create(private=False, room_id=room_id, name=name, description=description)
		channel.users.set(users)
		channel.creator = request.user.id
		channel.save()
		
		return JsonResponse({'success': True, 'message': 'The chat group is created', 'room_id': room_id}, status=200)


def room(request, room_id):
	if request.method == 'GET':

		# Update the user status
		if request.user.is_authenticated:
			request.user.set_status('chat:' + room_id)

		return render(request, 'base.html')