import logging, os
import requests
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import CustomUser
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from ..forms import LoginForm, SignUpForm, EditProfileForm
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_protect
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ..models import Notification, Channel


# 42 API
API_USER = 'https://api.intra.42.fr/v2/me'
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')


# Functions
@csrf_protect
def sign_in(request):
	if request.method == 'GET':
		form = LoginForm()
		return render(request, 'users/sign_in.html', {'form': form})
	
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
				login(request, user)
				return redirect('pong')
			else:
				messages.error(request, "Invalid credentials")
				return redirect('sign_in')

		messages.error(request, "Form error, you need to provide all fields")

		return redirect('sign_in')


@csrf_protect
def sign_up(request):
	if request.method == 'GET':
		form = SignUpForm()
		return render(request, 'users/sign_up.html', {'form': form})
	
	elif request.method == 'POST':
		form = SignUpForm(request.POST)

		if form.is_valid():
			if CustomUser.objects.filter(email=form.cleaned_data['email']).exists():
				messages.error(request, "This email is already taken")
				return redirect('sign_up')
			elif CustomUser.objects.filter(username=form.cleaned_data['username']).exists():
				messages.error(request, "This username is already taken")
				return redirect('sign_up')
			elif len(form.cleaned_data['username']) < 4:
				messages.error(request, "Your username is too short (4 characters minimum)")
				return redirect('sign_up')
			# Create the user
			user = CustomUser.objects.create_user(
					username=form.cleaned_data['username'],
					email=form.cleaned_data['email'],
					password=form.cleaned_data['password'])
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

			# Join the general channel
			try:
				channel = Channel.objects.get(name="general")
				channel.users.add(user)
			except Channel.DoesNotExist:
				channel = Channel.objects.create(name="general", room_name="general")
				channel.users.set([user])
				channel.save()

			return redirect('pong')

		else:
			if 'username' in form.errors:
				messages.error(request, "Your username can't have special characters")
			elif 'email' in form.errors:
				messages.error(request, "You need to provide a valid email")
			else:
				messages.error(request, "You need to provide all fields")
	return redirect('sign_up')


def sign_out(request):
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
 
	if request.user.is_authenticated:
		logout(request)
	
	return redirect('sign_in')


def ft_api(request):
	protocol = request.scheme
	port = '%3A8001' if protocol == "https" else '%3A8000'
	api_url = "https://api.intra.42.fr/oauth/authorize?client_id=" + CLIENT_ID + "&redirect_uri=" + \
	protocol + "%3A%2F%2Flocalhost" + \
	port + "%2Fcheck_authorize%2F&response_type=code"
	return redirect(api_url)


def	check_authorize(request):
	if request.method == 'GET' and 'error' in request.GET:
		return redirect('sign_in')
	if request.method == 'GET' and 'code' in request.GET:
		code = request.GET['code']
	response_token = handle_42_callback(request, code)
	response_data = make_api_request_with_token(API_USER, response_token)
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
		response = requests.get(photo_url)
		img = Image.open(BytesIO(response.content))
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
		
		# Join the general channel
		try:
			channel = Channel.objects.get(name="general")
			channel.users.add(user)
		except Channel.DoesNotExist:
			channel = Channel.objects.create(name="general", room_name="general")
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
			logging.error(f"Erreur de requête API: {response.status_code}")
			logging.error(response.text)
			return None
	except requests.RequestException as e:
		logging.error(f"Erreur de requête API: {e}")
		return None


def handle_42_callback(request, code):
	port = '8001' if request.scheme == 'https' else '8000'
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
		logging.info(f" error: {response.status_code}")
		logging.info(f" error: {response.text}")
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
		return redirect('sign_in')
	return redirect('profile', username=request.user.username)


@csrf_protect
def profile(request, username):
	if not request.user.is_authenticated:
		return redirect('sign_in')

	photo_name = request.user.photo.name

	# get the user
	User = get_user_model()
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return redirect('users')

	# get the room_name where the user and I are
	room = None
	channels = list(request.user.channels.all())
	for channel in channels:
		if channel.other_name == user.username or channel.name == user.username:
			room = channel.room_name
			break

	if request.method == 'GET':
		form = EditProfileForm(instance=request.user)
		context = {	'form':form,
					'user':user,
					'room':room}
		return render(request, 'profile.html', context)
	
	elif request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES, instance=request.user)
		context = {	'form':form,
					'user':user,
					'room':room}
		
		if form.is_valid():
			if request.user.photo and request.user.photo.name != photo_name:
				default_storage.delete(request.user.photo.path)
			elif len(form.cleaned_data['username']) < 4:
				messages.error(request, "Your username is too short (4 characters minimum)")
				return redirect('profile', username=username)
			form.save()
			messages.success(request, 'Your informations have been updated')
			return redirect('profile', username=request.user.username)
		
		else:
			if 'photo' in form.errors:
				messages.error(request, 'Please enter a valid picture')
			elif User.objects.filter(username=request.POST['username']).exists():
				messages.error(request, 'This username is already taken')
			else:
				messages.error(request, 'Please enter a valid username')
			return redirect('profile', username=username)

	return redirect('profile', username=username)


def users(request):
	if not request.user.is_authenticated:
		return redirect('sign_in')
	
	# Get all users and the friends
	User = get_user_model()
	all_users = User.objects.all()

	friends = []
	for user in all_users:
		if user.id in request.user.follows:
			friends.append(user)

	context = {'all_users':all_users, 'friends':friends}

	if request.method == 'GET':
		return render(request, 'users.html', context)
	elif request.method == 'POST':
		return redirect('users')


def follow(request, id):
	if not request.user.is_authenticated:
		return redirect('sign_in')

	# Check if the user exist and if he is not already followed
	User = get_user_model()
	try:
		userTo = User.objects.get(id=id)
		if id in request.user.follows:
			raise ValueError
	except (User.DoesNotExist, ValueError):
		return redirect('users')
	
	notification = Notification(user=userTo, message=f"{request.user.username} is now following you.")
	notification.save()
 
	request.user.follows.append(id)
	request.user.save()
	
	return redirect('profile', username=userTo.username)


def unfollow(request, id):
	if not request.user.is_authenticated:
		return redirect('sign_in')
	
	# Check if the user exist and if he is followed
	User = get_user_model()
	try:
		userTo = User.objects.get(id=id)
		if id not in request.user.follows:
			raise ValueError
	except (User.DoesNotExist, ValueError):
		return redirect('users')

	request.user.follows.remove(id)
	request.user.save()

	return redirect('profile', username=userTo.username)


def block(request, id):
	if not request.user.is_authenticated:
		return redirect('sign_in')

	# Check if the user exist and if he is not already blocked
	User = get_user_model()
	try:
		userTo = User.objects.get(id=id)
		if id in request.user.blockedUsers:
			raise ValueError
	except (User.DoesNotExist, ValueError):
		return redirect('users')
	
	# Unfollow the user if he is in the follows list
	if id in request.user.follows:
		request.user.follows.remove(id)
 
	# Block the user
	request.user.blockedUsers.append(id)
	request.user.save()

	return redirect('profile', username=userTo.username)


def unblock(request, id):
	if not request.user.is_authenticated:
		return redirect('sign_in')
	
	# Check if the user exist and if he is blocked
	User = get_user_model()
	try:
		userTo = User.objects.get(id=id)
		if id not in request.user.blockedUsers:
			raise ValueError
	except (User.DoesNotExist, ValueError):
		return redirect('users')

	# Unblock the user
	request.user.blockedUsers.remove(id)
	request.user.save()

	return redirect('profile', username=userTo.username)