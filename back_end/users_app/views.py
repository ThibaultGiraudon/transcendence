import requests
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from users_app.models import CustomUser
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from .forms import LoginForm, SignUpForm, EditProfileForm
from django.views.decorators.csrf import csrf_protect

API_URL = "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-4bc482d21834a4addd9108c8db4a5f99efb73b172f1a4cb387311ee09a26173c&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fcheck_authorize%2F&response_type=code"
API_USER = 'https://api.intra.42.fr/v2/me'
token = '690c107e335181f7039f3792799aebb1fa4d55b320bd232dd68877c0cc13545d'

@csrf_protect
def sign_in(request):
	"""
	Try to login in the user
 
	Arguments:
		????request: a url request????
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
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(request,username=username, password=password)
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
		????request: an url request????
	Returns:
		sign_in page : all fields are filled
		sign_up page : an error occured
	"""
	if request.method == 'GET':
		form = SignUpForm()
		return render(request, 'users/sign_up.html', {'form': form})
	
	elif request.method == 'POST':
		form = SignUpForm(request.POST)
		
		logging.info("-----------------")
		logging.info("Create user")
		if form.is_valid():
			user = CustomUser.objects.create_user(
					username=form.cleaned_data['username'],
					email=form.cleaned_data['email'],
					password=form.cleaned_data['password'])
			logging.info("-----------------")
			logging.info("User created")
			user.save()
			logging.info("-----------------")
			logging.info("User saved")
			return redirect('sign_in')
	
	messages.error(request, "Form error")
	return redirect('sign_up')


def sign_out(request):
	"""
	Logout the user
 
	Arguments:
		request: the user who should be delogged
	Returns:
		sign_in page
	"""
	if request.user.is_authenticated:
		logout(request)
	
	return redirect('sign_in')


def ft_api(request):
	return redirect(API_URL)


def	check_authorize(request):
	"""
	Check if the user authorize the 42's connection or not
 
	Arguments:
		????request: an url request????
	Returns:
		pong page : the user authorize the connection
		sign_in page : the user refuse the connection
	"""
	if request.method == 'GET' and 'error' in request.GET:
		return redirect('sign_in')
	if request.method == 'GET' and 'code' in request.GET:
		code = request.GET['code']
	response_token = handle_42_callback(code)
	response_data = make_api_request_with_token(API_USER, response_token)
	connect_42_user(request, response_data)
	return redirect('pong')


def	connect_42_user(request, response_data):
	"""
	Create user if the user connect for the first time
	Connect user

	Arguments:
		request : ????
		response_data : json data
	"""	
	logging.info("----------------------")
	logging.info(response_data['login'])
	user = authenticate_custom_user(
	 			email=response_data['email'], 
				username=response_data['login'])
	if user:
		logging.info("----------------------")
		logging.info("User logged\n")
		login(request, user)
	else :
		logging.info("----------------------")
		logging.info("Try Create User")
		user = CustomUser.objects.create(
	  				username=response_data['login'],
		  			email=response_data['email'],
	   				photo_url=response_data['image']['link'])
		user.save()
		logging.info("----------------------")
		logging.info("User created")
		user = authenticate_custom_user(
	  				email=response_data['email'], 
					username=response_data['login'],
					)
		if user:
			login(request, user)
			logging.info("----------------------")
			logging.info("User logged")


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


def handle_42_callback(code):
	"""
	Ask 42 api for token thanks to the code replied after the redirection
 
	Arguments:
		code : the replied code from 42 redirection
	Returns:
		None : the request failed
		token : the requet succeed
	"""
	token_url = "https://api.intra.42.fr/oauth/token"
	token_params = {
		'grant_type': 'authorization_code',
		'client_id': 'u-s4t2ud-4bc482d21834a4addd9108c8db4a5f99efb73b172f1a4cb387311ee09a26173c',
		'client_secret': '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',
		'code': code,
		'redirect_uri': 'http://localhost:8000/check_authorize/'
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


def authenticate_custom_user(email, username):
	"""
	Authenticate function without password
 
	Arguments:
		email : the email of the user who want to connect
		username : the username of the user who want to connect

	Returns:
		None : the user isn't registered
		user : the user exist
	"""
	UserModel = get_user_model()

	try:
		user = UserModel.objects.get(email=email, username=username)
		return user
	except UserModel.DoesNotExist:
		return None


def profile(request):
	User = get_user_model()
	all_users = User.objects.all()
	if request.method == 'GET':
		form = EditProfileForm(instance=request.user)
		context = {	'all_users':all_users,
					'form':form}
		return render(request, 'profile.html', context)
	elif request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)
		context = {	'all_users':all_users,
					'form':form}
		if form.is_valid():
			form.save()
			messages.success(request, 'Your username is updated successfuly')
			return render(request, 'profile.html', context)
		messages.error(request, "Form error, you need to provide all fields")
		return redirect('profile')
	return render(request, 'profile.html', context)