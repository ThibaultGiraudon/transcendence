# Dependencies
import os
import logging
import requests
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from users_app.models import CustomUser
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from .forms import LoginForm, SignUpForm, EditProfileForm
from django.conf import settings
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_protect

# 42 API
API_URL = "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-4bc482d21834a4addd9108c8db4a5f99efb73b172f1a4cb387311ee09a26173c&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fcheck_authorize%2F&response_type=code"
API_URR = "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-4bc482d21834a4addd9108c8db4a5f99efb73b172f1a4cb387311ee09a26173c&redirect_uri=https%3A%2F%2Flocalhost%3A8001%2Fcheck_authorize%2F&response_type=code"
API_URU = "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-4bc482d21834a4addd9108c8db4a5f99efb73b172f1a4cb387311ee09a26173c&redirect_uri=https%3A%2F%2Flocalhost%3A8001%2Fcheck_authorize%2F&response_type=code"
API_USER = 'https://api.intra.42.fr/v2/me'
token = '690c107e335181f7039f3792799aebb1fa4d55b320bd232dd68877c0cc13545d'

# Functions
@csrf_protect
def sign_in(request):
	"""
	Try to login in the user
 
	Arguments:
		request: ???
	Returns:
		pong page : the credential are good
		sign_in page : the credential are wrong
	"""

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
				login(request, user)
				return redirect('pong')
			else:
				messages.error(request, "Invalid credentials")
				return redirect('sign_in')

		messages.error(request, "Form error, you need to provide all fields")
		return redirect('sign_in')


@csrf_protect
def sign_up(request):
	"""
	Create a new user
 
	Arguments:
		request: ???
	Returns:
		sign_in page : all fields are filled
		sign_up page : an error occured
	"""

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
			
			user = CustomUser.objects.create_user(
					username=form.cleaned_data['username'],
					email=form.cleaned_data['email'],
					password=form.cleaned_data['password'])
			user.save()
			login(request, user)
			return redirect('pong')
	
	messages.error(request, "You need to provide all fields")
	return redirect('sign_up')


def sign_out(request):
	"""
	Log out the user
 
	Arguments:
		request: ???
	Returns:
		sign_in page
	"""

	if request.user.is_authenticated:
		logout(request)
	
	return redirect('sign_in')


def ft_api(request):
	logging.info("------------------\nIS_SECURE")
	logging.info(request.is_secure)
	logging.info("------------------\nSCHEME")
	logging.info(request.scheme)
	protocol = request.scheme
	port = '%3A8001' if protocol == "https" else '%3A8000'
	api_url = "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-4bc482d21834a4addd9108c8db4a5f99efb73b172f1a4cb387311ee09a26173c&redirect_uri=" + \
	protocol + "%3A%2F%2Flocalhost" + \
	port + "%2Fcheck_authorize%2F&response_type=code"
	logging.info("--------------------\nAPI_URL")
	logging.info(api_url)
	return redirect(api_url)


def	check_authorize(request):
	"""
	Check if the user authorize the 42's connection or not
 
	Arguments:
		request: ???
	Returns:
		pong page : the user authorize the connection
		sign_in page : the user refuse the connection
	"""

	if request.method == 'GET' and 'error' in request.GET:
		return redirect('sign_in')
	if request.method == 'GET' and 'code' in request.GET:
		code = request.GET['code']
	response_token = handle_42_callback(request, code)
	response_data = make_api_request_with_token(API_USER, response_token)
	connect_42_user(request, response_data)
	return redirect('pong')


def	connect_42_user(request, response_data):
	"""
	Create user if the user connect for the first time

	Arguments:
		request : ????
		response_data : json data
	"""

	user = authenticate_42_user(email=response_data['email'])
	if user:
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


def make_api_request_with_token(api_url, token):
	"""
	Request for 42 api
 
	Arguments:
		api_url : the api url request
		token : token to access the api

	Returns:
		None : the request faild
		json data : the request succeed
	"""

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
	"""
	Ask 42 api for token thanks to the code replied after the redirection
 
	Arguments:
		request : ???
		code : the replied code from 42 redirection
	Returns:
		None : the request failed
		token : the requet succeed
	"""
	port = '8001' if request.scheme == 'https' else '8000'
	redirect_uri = request.scheme + '://localhost:' + port + '/check_authorize/'
	token_url = "https://api.intra.42.fr/oauth/token"
	logging.info("-----------------\nREDIRECT_URI")
	logging.info(redirect_uri)
	token_params = {
		'grant_type': 'authorization_code',
		'client_id': 'u-s4t2ud-4bc482d21834a4addd9108c8db4a5f99efb73b172f1a4cb387311ee09a26173c',
		'client_secret': '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',
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
	"""
	Authenticate function with email and password
 
	Arguments:
		email : the email of the user who want to connect
		password : the password of the user who want to connect

	Returns:
		None : the user isn't registered
		user : the user exist
	"""

	User = get_user_model()

	try:
		user = User.objects.get(email=email)
		if user.check_password(password):
			return user
	except User.DoesNotExist:
		return None


def authenticate_42_user(email):
	"""
	Authenticate function without password
 
	Arguments:
		email : the email of the 42 user who want to connect

	Returns:
		None : the user isn't registered
		user : the user exist
	"""

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
	User = get_user_model()

	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return redirect('users')

	if request.method == 'GET':
		form = EditProfileForm(instance=request.user)
		context = {	'form':form,
					'user':user}
		return render(request, 'profile.html', context)
	
	elif request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES, instance=request.user)
		context = {	'form':form,
					'user':user}
		
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
	
	User = get_user_model()
	all_users = User.objects.all()
	context = {'all_users':all_users}

	if request.method == 'GET':
		return render(request, 'users.html', context)
	elif request.method == 'POST':
		return redirect('users')