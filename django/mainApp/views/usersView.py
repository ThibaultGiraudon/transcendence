import os
import requests
import imghdr
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from ..models import CustomUser
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from ..models import Notification, Channel
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
import urllib.request, json, base64


from mainApp.models import Player
from mainApp.views.utils import redirectPage, renderError


# 42 API
API_USER = 'https://api.intra.42.fr/v2/me'
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')


# Views
@ensure_csrf_cookie
def sign_in(request):
	if request.method == 'GET':
		get_token(request)
		return render(request, 'base.html')

	elif request.method == 'POST':
		# Get the data
		data = json.loads(request.body)
		email = data.get('email')
		password = data.get('password')

		# Authenticate the user
		user = authenticate_custom_user(email=email, password=password)

		if user == 'emailError':
			return JsonResponse({"success": False, "email": "Invalid email"}, status=401)
		elif user == 'passwordError':
			return JsonResponse({"success": False, "password": "Invalid password"}, status=401)
		else:
			login(request, user)

			# Update the user status
			user.set_status("online")

			return JsonResponse({"success": True, "message": "Successful login"}, status=200)


@ensure_csrf_cookie
def sign_up(request):
	if request.method == 'GET':
		get_token(request)
		return render(request, 'base.html')
	
	elif request.method == 'POST':
		# Get the data
		data = json.loads(request.body)
		username = data.get('username')
		email = data.get('email')
		password = data.get('password')

		if CustomUser.objects.filter(email=email).exists():
			return JsonResponse({"success": False, "email": "This email is already taken"}, status=401)

		if CustomUser.objects.filter(username=username).exists():
			return JsonResponse({"success": False, "username": "This username is already taken"}, status=401)
		
		elif len(username) < 4:
			return JsonResponse({"success": False, "username": "Your username is too short (4 characters minimum)"}, status=401)
		
		elif len(username) > 20:
			return JsonResponse({"success": False, "username": "Your username is too long (20 characters maximum)"}, status=401)

		# Create the user
		user = CustomUser.objects.create_user(
				username=username,
				email=email,
				password=password)
		
		user.save()

		# Login the user
		login(request, user)

		user.set_status("online")

		# Join the General channel
		try:
			channel = Channel.objects.get(room_id="general")
			channel.users.add(user)
		except Exception as e:
			channel = Channel.objects.create(name="General", room_id="general")
			channel.users.set([user])
			channel.save()

		return JsonResponse({"success": True, "message": "Successful sign up"}, status=200)


@ensure_csrf_cookie
def profile(request, username):
	if request.method == 'GET':
		return render(request, 'base.html')

	elif request.method == 'POST':
		# Get the data
		data = json.loads(request.body)
		new_username = data.get('new_username')
		photo = data.get('photo')

		# Check if the username is valid
		if new_username == request.user.username:
			pass
		elif len(new_username) < 4:
			return JsonResponse({"success": False, "username": "This username is too short (4 characters minimum)"}, status=401)
		elif len(new_username) > 20:
			return JsonResponse({"success": False, "username": "This username is too long (20 characters maximum)"}, status=401)
		elif ' ' in new_username:
			return JsonResponse({"success": False, "username": "This username cannot contain space"}, status=401)
		elif any(char.isdigit() for char in new_username):
			return JsonResponse({"success": False, "username": "This username cannot contain special characters"}, status=401)
		elif CustomUser.objects.filter(username=new_username).exists():
			return JsonResponse({"success": False, "username": "This username is already taken"}, status=401)
		else:
			request.user.username = new_username
			request.user.save()
		
		# Check if the photo is valid
		if photo:
			# Delete the old photo
			if request.user.photo and request.user.photo.path != 'static/main/img/default.jpg':
				default_storage.delete(request.user.photo.path)
			
			# Decode the Base64 photo
			try:
				photo_data = base64.b64decode(photo)
				photo_image = Image.open(BytesIO(photo_data))
			except Exception as e:
				return JsonResponse({"success": False, "message": "Invalid image file"}, status=401)

			# Determine the image file type
			image_type = imghdr.what(None, photo_data)
			if image_type is None:
				return JsonResponse({"success": False, "message": "Invalid image file"}, status=401)
			
			# Save the new photo
			photo_temp = BytesIO()
			photo_image.save(photo_temp, format=image_type.upper())
			photo_temp.seek(0)
			request.user.photo.save(f"{request.user.email}.{image_type}", File(photo_temp), save=True)
			request.user.save()

		return JsonResponse({"success": True, "message": "Successful profile update"}, status=200)
	
	else:
		return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)
	


def ft_api(request):
	protocol = request.scheme
	port = '%3A8443' if protocol == "https" else '%3A8000'
	host = request.get_host().split(':')[0]
	api_url = "https://api.intra.42.fr/oauth/authorize?client_id=" + CLIENT_ID + "&redirect_uri=" + \
	protocol + f"%3A%2F%2F{host}" + \
	port + "%2Fcheck_authorize%2F&response_type=code"

	return redirect(api_url)


def	check_authorize(request):
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
		user.set_status("online")

		login(request, user)

	else:
		photo_url = response_data['image']['link']

		with urllib.request.urlopen(photo_url) as url:
			with Image.open(BytesIO(url.read())) as img:
				img_io = BytesIO()
				img.save(img_io, format='JPEG')

		player = Player.objects.create(currentGameID=None)
		user = CustomUser.objects.create(
			username=response_data['login'],
			email=response_data['email'],
			player=player
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
	host = request.get_host().split(':')[0]
	redirect_uri = request.scheme + f"://{host}:" + port + '/check_authorize/'
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
		else:
			return 'passwordError'
	except User.DoesNotExist:
		return 'emailError'


def authenticate_42_user(email):
	User = get_user_model()

	try:
		user = User.objects.get(email=email)
		return user
	except User.DoesNotExist:
		return None


def users(request):
	if request.method == 'GET':
		return render(request, 'base.html')


def notifications(request):
	if request.method == 'GET':
		return render(request, 'base.html')