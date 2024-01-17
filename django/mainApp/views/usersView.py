import logging, os
import requests
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from ..models import CustomUser
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from ..forms import LoginForm, SignUpForm, EditProfileForm
from django.core.files.storage import default_storage
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ..models import Notification, Channel
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
import urllib.request

from mainApp.views.utils import renderPage, redirectPage, renderError


# 42 API
API_USER = 'https://api.intra.42.fr/v2/me'
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')


# Views
@ensure_csrf_cookie
def sign_in(request):
	if request.method == 'GET':
		return renderPage(request, 'users/sign_in.html', {'form': LoginForm()})
	
	elif request.method == 'POST':
		form = LoginForm(request.POST)
		
		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			user = authenticate_custom_user(email=email, password=password)

			if user:
				# Update the user status
				user.status = "online"
				user.save()

				# Send the status to the channel layer
				channel_layer = get_channel_layer()
				async_to_sync(channel_layer.group_send)(
					'status',
					{
						'type': 'status_update',
						'username': user.username,
						'id': user.id,
						'status': 'online'
					}
				)

				# Login the user
				login(request, user)

				return JsonResponse({'success': True, 'redirect': '/pong/'})
			
			else:
				form.add_error('password', 'Invalid credentials')
				return JsonResponse({'success': False, 'errors': form.errors.get_json_data()})
		
		else:
			form.add_error('password', 'Invalid credentials')
			return JsonResponse({'success': False, 'errors': form.errors.get_json_data()})


@ensure_csrf_cookie
def sign_up(request):
	if request.method == 'GET':
		return renderPage(request, 'users/sign_up.html', {'form': SignUpForm()})
	
	elif request.method == 'POST':
		form = SignUpForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')

			if CustomUser.objects.filter(email=email).exists():
				form.add_error('email', "This email is already taken")
				return JsonResponse({'success': False, 'errors': form.errors.get_json_data()})

			if CustomUser.objects.filter(username=username).exists():
				form.add_error('username', "This username is already taken")
				return JsonResponse({'success': False, 'errors': form.errors.get_json_data()})

			if len(username) < 4:
				form.add_error('username', 'Your username is too short (4 characters minimum)')
				return JsonResponse({'success': False, 'errors': form.errors.get_json_data()})
	
			# Create the user
			user = CustomUser.objects.create_user(
					username=username,
					email=email,
					password=password)
			user.save()
			login(request, user)

			# Send the status to the channel layer
			channel_layer = get_channel_layer()
			async_to_sync(channel_layer.group_send)(
				'status',
				{
					'type': 'status_update',
					'username': request.user.username,
					'id': request.user.id,
					'status': 'online'
				}
			)

			# Join the General channel
			try:
				channel = Channel.objects.get(room_id="general")
				channel.users.add(user)
			except Exception as e:
				channel = Channel.objects.create(name="General", room_id="general")
				channel.users.set([user])
				channel.save()

			return JsonResponse({'success': True, 'redirect': '/pong/'})

		else:
			return JsonResponse({'success': False, 'errors': form.errors.get_json_data()})


def sign_out(request):
	if request.user.is_authenticated:
		# Update the user status
		request.user.status = "offline"
		request.user.save()

		# Send the status to the channel layer
		channel_layer = get_channel_layer()
		async_to_sync(channel_layer.group_send)(
			'status',
			{
				'type': 'status_update',
				'username': request.user.username,
				'id': request.user.id,
				'status': 'offline'
			}
		)
	
		# Logout the user
		logout(request)
	
	return redirectPage(request, '/sign_in/')


def ft_api(request):
	protocol = request.scheme
	port = '%3A8443' if protocol == "https" else '%3A8000'

	api_url = "https://api.intra.42.fr/oauth/authorize?client_id=" + CLIENT_ID + "&redirect_uri=" + \
	protocol + "%3A%2F%2Flocalhost" + \
	port + "%2Fcheck_authorize%2F&response_type=code"

	scheme = request.is_secure() and "https" or "http"

	return redirect(api_url)


def	check_authorize(request):
	if request.method == 'GET' and 'error' in request.GET:
		return redirect('sign_in')
	
	if request.method == 'GET' and 'code' in request.GET:
		code = request.GET['code']
	
	response_token = handle_42_callback(request, code)
	if response_token is None:
		return renderError(request, 498, {'title':"The token has expired", 'infos':"Please contact the administrator"})
	
	response_data = make_api_request_with_token(API_USER, response_token)
	if response_data is None:
		return renderError(request, 401, {'title':"The 42 API is down", 'infos':"Please contact the administrator"})
	
	connect_42_user(request, response_data)

	return redirect('pong')


def	connect_42_user(request, response_data):
	user = authenticate_42_user(email=response_data['email'])
	
	if user:
		user.status = "online"
		channel_layer = get_channel_layer()
		async_to_sync(channel_layer.group_send)(
			'status',
			{
				'type': 'status_update',
				'username': user.username,
				'id': user.id,
				'status': 'online'
			}
		)
		user.save()
		login(request, user)

	else:
		photo_url = response_data['image']['link']

		with urllib.request.urlopen(photo_url) as url:
			with Image.open(BytesIO(url.read())) as img:
				img_io = BytesIO()
				img.save(img_io, format='JPEG')

		user = CustomUser.objects.create(
			username=response_data['login'],
			email=response_data['email']
		)
		user.photo.save(f"{response_data['email']}.jpg", ContentFile(img_io.getvalue()), save=True)
		user.save()
		user = authenticate_42_user(email=response_data['email'])
		if user:
			login(request, user)
		
		# Join the General channel
		try:
			channel = Channel.objects.get(room_id="general")
			channel.users.add(user)
		except Exception as e:
			channel = Channel.objects.create(name="General", room_id="general")
			channel.users.set([user])
			channel.save()


def make_api_request_with_token(api_url, token):
	headers = {
		'Authorization': f'Bearer {token}',
	}

	try:
		response = requests.get(api_url, headers=headers)

		if response.status_code == 200:
			data = response.json()
			return data
		else:
			return None
	except requests.RequestException as e:
		return None


def handle_42_callback(request, code):
	port = '8443' if request.scheme == 'https' else '8000'
	redirect_uri = request.scheme + '://localhost:' + port + '/check_authorize/'
	token_url = "https://api.intra.42.fr/oauth/token"
	token_params = {
		'grant_type': 'authorization_code',
		'client_id': CLIENT_ID,
		'client_secret': CLIENT_SECRET,
		'code': code,
		'redirect_uri': redirect_uri
	}

	response = requests.post(token_url, data=token_params)

	if response.status_code == 200:
		token_data = response.json()
		access_token = token_data['access_token']
		return access_token 
	else:
		return None


def authenticate_custom_user(email, password):
	User = get_user_model()

	try:
		user = User.objects.get(email=email)
		if user.check_password(password):
			return user
	except User.DoesNotExist:
		return None


def authenticate_42_user(email):
	User = get_user_model()

	try:
		user = User.objects.get(email=email)
		return user
	except User.DoesNotExist:
		return None


def profile_me(request):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')
	
	return redirectPage(request, '/profile/' + request.user.username)


@ensure_csrf_cookie
def profile(request, username):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')

	# Get the photo name to delete it if the user change his photo
	photo_name = request.user.photo.name

	# Get the user of the profile
	User = get_user_model()
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return redirectPage(request, '/users/')

	# Get the private chat between the request.user and the user
	room = None
	channels = list(request.user.channels.all())
	for channel in channels:
		if channel.private and len(channel.users.all()) == 2 and user in channel.users.all():
			room = channel.room_id
			break

	if request.method == 'GET':
		form = EditProfileForm(instance=request.user)
		context = {
			'form': form,
			'user': user,
			'room': room
		}
		
		return renderPage(request, 'profile.html', context)
	
	elif request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES, instance=request.user)
		
		if form.is_valid():
			if request.user.photo and request.user.photo.name != photo_name:
				default_storage.delete(request.user.photo.path)
			elif len(form.cleaned_data['username']) < 4:
				form.add_error('username', 'Your username is too short (4 characters minimum)')
				return JsonResponse({'success': False, 'redirect': '/profile/' + username, 'errors': form.errors.get_json_data()})
			elif ' ' in form.cleaned_data['username']:
				form.add_error('username', 'Your username cannot contain space')
				return JsonResponse({'success': False, 'redirect': '/profile/' + username, 'errors': form.errors.get_json_data()})
			elif not form.cleaned_data['username'].isalnum():
				form.add_error('username', 'Your username cannot contain special characters')
				return JsonResponse({'success': False, 'redirect': '/profile/' + username, 'errors': form.errors.get_json_data()})
			
			form.save()
			return JsonResponse({'success': True, 'redirect': '/profile/' + form.cleaned_data['username']})
		
		else:
			if 'photo' in form.errors:
				form.add_error('photo', 'Please enter a valid picture')
			elif User.objects.filter(username=request.POST['username']).exists():
				form.add_error('username', 'This username is already taken')
			else:
				form.add_error('username', 'Please enter a valid username')

			return JsonResponse({'success': False, 'redirect': '/profile/' + username, 'errors': form.errors.get_json_data()})

	return JsonResponse({'success': False, 'redirect': '/profile/' + username})


def users(request):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')
	
	# Get all users and the friends
	User = get_user_model()
	all_users = User.objects.all()

	# Hide the current user
	all_users = all_users.exclude(id=request.user.id)

	if request.method == 'GET':
		friends = []

		for user in all_users:
			if user.id in request.user.follows:
				friends.append(user)

		context = {'all_users':all_users, 'friends':friends}

		return renderPage(request, 'users.html', context)
	
	elif request.method == 'POST':
		return redirectPage(request, '/users/')


def follow(request, id):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')

	# Check if the user exist and if he is not already followed
	User = get_user_model()
	try:
		userTo = User.objects.get(id=id)
		if id in request.user.follows:
			raise ValueError
	except (User.DoesNotExist, ValueError):
		return redirectPage(request, '/users/')
	
	notification = Notification(user=userTo, message=f"{request.user.username} is now following you.")
	notification.save()
 
	request.user.follows.append(id)
	request.user.save()
	
	return redirectPage(request, '/profile/' + userTo.username)


def unfollow(request, id):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')
	
	# Check if the user exist and if he is followed
	User = get_user_model()
	try:
		userTo = User.objects.get(id=id)
		if id not in request.user.follows:
			raise ValueError
	except (User.DoesNotExist, ValueError):
		return redirectPage(request, '/users/')

	request.user.follows.remove(id)
	request.user.save()

	return redirectPage(request, '/profile/' + userTo.username)


def block(request, id):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')

	# Check if the user exist and if he is not already blocked
	User = get_user_model()
	try:
		userTo = User.objects.get(id=id)
		if id in request.user.blockedUsers:
			raise ValueError
	except (User.DoesNotExist, ValueError):
		return redirectPage(request, '/users/')
	
	# Unfollow the user if he is in the follows list
	if id in request.user.follows:
		request.user.follows.remove(id)
 
	# Block the user
	request.user.blockedUsers.append(id)
	request.user.save()

	return redirectPage(request, '/profile/' + userTo.username)


def unblock(request, id):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')
	
	# Check if the user exist and if he is blocked
	User = get_user_model()
	try:
		userTo = User.objects.get(id=id)
		if id not in request.user.blockedUsers:
			raise ValueError
	except (User.DoesNotExist, ValueError):
		return redirectPage(request, '/users/')

	# Unblock the user
	request.user.blockedUsers.remove(id)
	request.user.save()

	return redirectPage(request, '/profile/' + userTo.username)


def get_username(request, id):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')

	# Check if the user exist
	User = get_user_model()
	try:
		user = User.objects.get(id=id)
	except User.DoesNotExist:
		return redirectPage(request, '/users/')
	
	return JsonResponse({'username': user.username})