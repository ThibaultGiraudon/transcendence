import requests
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from users_app.models import CustomUser
from django.contrib.auth import login, logout, authenticate
from .forms import LoginForm, SignUpForm
from django.views.decorators.csrf import csrf_protect

API_URL = "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-4bc482d21834a4addd9108c8db4a5f99efb73b172f1a4cb387311ee09a26173c&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fcheck_authorize%2F&response_type=code"
API_USER = 'https://api.intra.42.fr/v2/me'
token = '4b05a7f238c5c1f4191d856d2f001d1ded53ac5a13b77b197bb4f8150ac2efea'

@csrf_protect
def sign_in(request):
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
	# Logout the current user
	if request.user.is_authenticated:
		logout(request)
	
	return redirect('sign_in')


def ft_api(request):
	return redirect(API_URL)


def	check_authorize(request):
	if request.method == 'GET' and 'error' in request.GET:
		return redirect('sign_in')
	if request.method == 'GET' and 'code' in request.GET:
		code = request.GET['code']
	response_token = handle_42_callback(code)
	response_data = make_api_request_with_token(API_USER, response_token)
	# logging.info("----------------------")
	# logging.info(response_data['login'])
	# user = authenticate(request, username=response_data['login'])
	# if user:
	# 	logging.info("----------------------")
	# 	logging.info("User logged\n")
	# 	login(request, user)
	# else :
	# 	logging.info("----------------------")
	# 	logging.info("Try Create User")
	# 	user = User.objects.create(
    #   				username=response_data['login'],
    #       			email=response_data['email'])
	# 	user.save()
	# 	logging.info("----------------------")
	# 	logging.info("User created")
	# 	user = authenticate(request, username=response_data['login'])
	# 	if user:
	# 		login(request, user)
	# 		logging.info("----------------------")
	# 		logging.info("User logged")
	return redirect('pong')

def make_api_request_with_token(api_url, token):
	# Définir l'en-tête avec le token d'authentification
	headers = {
		'Authorization': f'Bearer {token}',
		# 'Content-Type': 'application/json',  # Adapté selon les besoins de l'API
	}

	try:
		# Effectuer la requête GET (ou POST, PUT, etc.) avec l'en-tête
		response = requests.get(api_url, headers=headers)

		# Vérifier si la requête a réussi (statut 200)
		if response.status_code == 200:
			# Traitement de la réponse JSON, si nécessaire
			data = response.json()
			return data
		else:
			# Gérer les erreurs de requête ici
			logging.error(f"Erreur de requête API: {response.status_code}")
			logging.error(response.text)
			return None
	except requests.RequestException as e:
		# Gérer les erreurs d'exception ici
		logging.error(f"Erreur de requête API: {e}")
		return None


def handle_42_callback(code):
	# Récupérer le code d'autorisation de l'URL
	# Échanger le code d'autorisation contre un token d'accès
	token_url = "https://api.intra.42.fr/oauth/token"
	token_params = {
		'grant_type': 'authorization_code',
		'client_id': 'u-s4t2ud-4bc482d21834a4addd9108c8db4a5f99efb73b172f1a4cb387311ee09a26173c',
		'client_secret': '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',
		'code': code,
		'redirect_uri': 'http://localhost:8000/check_authorize/'
	}

	# Faire une demande POST pour obtenir le token d'accès
	response = requests.post(token_url, data=token_params)

	if response.status_code == 200:
		# L'exemple suppose que la réponse est en format JSON
		token_data = response.json()

		# Utiliser le token d'accès pour authentifier l'utilisateur
		access_token = token_data['access_token']

		# Effectuer des opérations d'authentification avec Django
		# ...
		return access_token  # Rediriger vers la page d'accueil après l'authentification
	else:
		# Gérer les erreurs d'authentification
		logging.info(f" error: {response.status_code}")
		logging.info(f" error: {response.text}")
		return None

# def user_profile(request):
    