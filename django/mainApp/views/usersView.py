import os
import re
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
from ..models import Channel
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import JsonResponse
import urllib.request, json, base64, uuid
from datetime import datetime

from mainApp.models import Player


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

			# Send an email to the user	
			if user.emailAlerts:
				now = datetime.now()
				date = now.strftime("%Y-%m-%d")
				time = now.strftime("%H:%M:%S")
			
				message = f"""
				<p>Hello <b>{user.username}</b>,</p>
				<p>A new connection to transcendence has just been recorded with your account.</p>
				<p>If you received this email by mistake, please ignore it.</p>

				<h3>Informations:</h3>
				<p>
				- <b>Date</b>: {date}<br>
				- <b>Time</b>: {time}<br>
				- <b>IP address</b>: {request.META.get('REMOTE_ADDR')}
				</p>

				<p>
				Have a good day,<br>
				<i>The transcendence team</i>
				</p>
				"""
				
				send_mail(
					'New connection to your account',
					message,
					'Transcendence Team <transcendence.42lyon.project@gmail.com>',
					[user.email],
					html_message=message,
					fail_silently=True,
				)

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

		if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
			return JsonResponse({"success": False, "email": "Invalid email format"}, status=401)
		elif CustomUser.objects.filter(email=email).exists():
			return JsonResponse({"success": False, "email": "This email is already taken"}, status=401)
		
		if CustomUser.objects.filter(username=username).exists():
			return JsonResponse({"success": False, "username": "This username is already taken"}, status=401)
		elif not re.match('^[a-zA-Z0-9-]*$', username):
			return JsonResponse({"success": False, "username": "This username cannot contain special characters"}, status=401)
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
		
		# Send an email to the user
		if user.emailAlerts:
			message = f"""
			<p>Hello <b>{user.username}</b>,</p>
			<p>
			Welcome to transcendence! We are glad to have you with us.</br>
			Feel free to explore the platform and join the different channels to chat with other users
			and play games.
			</p>
			<p>If you received this email by mistake, please ignore it.</p>

			<p>
			Have a good day,<br>
			<i>The transcendence team</i>
			</p>
			"""
			
			send_mail(
				'Welcome to transcendence',
				message,
				'Transcendence Team <transcendence.42lyon.project@gmail.com>',
				[user.email],
				html_message=message,
				fail_silently=True,
			)

		return JsonResponse({"success": True, "message": "Successful sign up"}, status=200)


@ensure_csrf_cookie
def reset_password(request):
	if request.method == 'GET':
		return render(request, 'base.html')

	elif request.method == 'POST':

		# Get the data
		data = json.loads(request.body)
		email = data.get('email')

		# Check if the email is valid
		if not len(email):
			return JsonResponse({"success": False, "email": "This email is empty"}, status=401)
		elif not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
			return JsonResponse({"success": False, "email": "Invalid email format"}, status=401)
		
		# Fake the success to avoid giving information about the registered emails
		elif not CustomUser.objects.filter(email=email).exists():
			return JsonResponse({"success": True, "message": "Successful email sent"}, status=200)

		# Check if the user is from 42
		user = CustomUser.objects.get(email=email)
		if user.is42:
			return JsonResponse({"success": False, "message": "This email is associated with a 42 account"}, status=401)

		# Send an email to the user
		resetPasswordID = str(uuid.uuid1())
		user.resetPasswordID = resetPasswordID
		user.save()

		if user.emailAlerts:
			message = f"""
			<p>Hello <b>{user.username}</b>,</p>
			<p>
			You recently requested to reset your password. If this was you, please click on the link below
			to reset your password. If you did not request this, please ignore this email.
			</p>
			
			<p>
			<a href="https://10.14.9.5:8443/reset_password_id/{user.resetPasswordID}">Reset your password</a>
			</p>
			
			<p>
			Have a good day,<br>
			<i>The transcendence team</i>
			</p>
			"""

			send_mail(
				'Reset your password',
				message,
				'Transcendence Team <transcendence.42lyon.project@gmail.com>',
				[user.email],
				html_message=message,
				fail_silently=True,
			)

		return JsonResponse({"success": True, "message": "Successful email sent"}, status=200)


@ensure_csrf_cookie
def reset_password_id(request, resetPasswordID):
	if request.method == 'GET':
		return render(request, 'base.html')

	elif request.method == 'POST':
		# Get the data
		data = json.loads(request.body)
		new_password = data.get('password')

		# Check if the password is valid
		if not len(new_password):
			return JsonResponse({"success": False, "password": "This password is empty"}, status=401)

		# Reset the password
		try:
			user = CustomUser.objects.get(resetPasswordID=resetPasswordID)
			user.resetPasswordID = ''
			user.set_password(new_password)
			user.save()
		except CustomUser.DoesNotExist:
			return JsonResponse({"success": False, "message": "Invalid reset password ID"}, status=401)

		# Send an email to the user	
		now = datetime.now()
		date = now.strftime("%Y-%m-%d")
		time = now.strftime("%H:%M:%S")
	
		message = f"""
		<p>Hello <b>{user.username}</b>,</p>
		<p>Your password has been successfully changed by the new one you provided.</p>
		<p>If you received this email by mistake, please ignore it.</p>

		<h3>Informations:</h3>
		<p>
		- <b>Date</b>: {date}<br>
		- <b>Time</b>: {time}<br>
		- <b>IP address</b>: {request.META.get('REMOTE_ADDR')}
		</p>

		<p>
		Have a good day,<br>
		<i>The transcendence team</i>
		</p>
		"""
		
		send_mail(
			'Successful password reset',
			message,
			'Transcendence Team <transcendence.42lyon.project@gmail.com>',
			[user.email],
			html_message=message,
			fail_silently=True,
		)

		return JsonResponse({"success": True, "message": "Successful password reset"}, status=200)


@ensure_csrf_cookie
def profile(request, username):
	if request.method == 'GET':
		return render(request, 'base.html')

	elif request.method == 'POST':
		# Get the data
		data = json.loads(request.body)
		new_username = data.get('new_username')
		photo = data.get('photo')
		new_email = data.get('new_email')
		new_password = data.get('new_password')
		emailAlerts = data.get('emailAlerts')

		# Validate the email alerts
		if emailAlerts is not None:
			if emailAlerts not in [True, False]:
				return JsonResponse({"success": False, "message": "Invalid email alerts value"}, status=401)
			else:
				request.user.emailAlerts = emailAlerts
				request.user.save()

		# Check if the username is valid
		if new_username == request.user.username:
			pass
		elif len(new_username) < 4:
			return JsonResponse({"success": False, "username": "This username is too short (4 characters minimum)"}, status=401)
		elif len(new_username) > 20:
			return JsonResponse({"success": False, "username": "This username is too long (20 characters maximum)"}, status=401)
		elif ' ' in new_username:
			return JsonResponse({"success": False, "username": "This username cannot contain space"}, status=401)
		elif not re.match('^[a-zA-Z0-9-]*$', new_username):
			return JsonResponse({"success": False, "username": "This username cannot contain special characters"}, status=401)
		elif CustomUser.objects.filter(username=new_username).exists():
			return JsonResponse({"success": False, "username": "This username is already taken"}, status=401)
		else:
			request.user.username = new_username
			request.user.save()
		
		# Check if the photo is valid
		if photo:
			# Delete the old photo
			if request.user.photo and request.user.photo.path != 'static/users/img/default.jpg':
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

		# Check if the email is valid
		old_email = request.user.email
		if new_email == request.user.email:
			pass
		elif not len(new_email):
			return JsonResponse({"success": False, "email": "This email is empty"}, status=401)
		elif not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", new_email):
			return JsonResponse({"success": False, "email": "Invalid email format"}, status=401)
		elif CustomUser.objects.filter(email=new_email).exists():
			return JsonResponse({"success": False, "email": "This email is already taken"}, status=401)
		else:
			# Change the status to offline
			request.user.set_status("offline")
			request.user.save()

			request.user.email = new_email
			request.user.save()
		
		# Check if the password is valid
		if not len(new_password):
			pass
		else:
			# Change the status to offline
			request.user.set_status("offline")
			request.user.save()

			request.user.set_password(new_password)
			request.user.save()
		
		# Send an email to the user
		if new_email != request.user.email or new_password:
			now = datetime.now()
			date = now.strftime("%Y-%m-%d")
			time = now.strftime("%H:%M:%S")
		
			message = f"""
			<p>Hello <b>{request.user.username}</b>,</p>
			"""

			if old_email != request.user.email:
				message += f"""
				<p>Your email has been successfully changed from <b>{old_email}</b> to <b>{new_email}</b>.</p>
				"""
			if new_password:
				message += f"""
				<p>Your password has been successfully changed.</p>
				"""

			message += f"""
			<p>If you received this email by mistake, please ignore it.</p>

			<h3>Informations:</h3>
			<p>
			- <b>Date</b>: {date}<br>
			- <b>Time</b>: {time}<br>
			- <b>IP address</b>: {request.META.get('REMOTE_ADDR')}
			</p>

			<p>
			Have a good day,<br>
			<i>The transcendence team</i>
			</p>
			"""
			
			send_mail(
				'Successful profile update',
				message,
				'Transcendence Team <transcendence.42lyon.project@gmail.com>',
				[old_email, request.user.email] if old_email != request.user.email else [request.user.email],
				html_message=message,
				fail_silently=True,
			)

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
		return redirect('token42')
	
	response_data = make_api_request_with_token(API_USER, response_token)
	if response_data is None:
		return redirect('down42')
	
	return connect_42_user(request, response_data)


def	connect_42_user(request, response_data):
	user = authenticate_42_user(email=response_data['email'])
	
	if user:
		if not user.is42:
			return redirect('used42')

		user.set_status("online")

		login(request, user)

		# Send an email to the user
		if user.emailAlerts:
			now = datetime.now()
			date = now.strftime("%Y-%m-%d")
			time = now.strftime("%H:%M:%S")

			message = f"""
			<p>Hello <b>{user.username}</b>,</p>
			<p>A new connection to transcendence has just been recorded with your account.</p>
			<p>If you received this email by mistake, please ignore it.</p>

			<h3>Informations:</h3>
			<p>
			- <b>Date</b>: {date}<br>
			- <b>Time</b>: {time}<br>
			- <b>IP address</b>: {request.META.get('REMOTE_ADDR')}
			</p>

			<p>
			Have a good day,<br>
			<i>The transcendence team</i>
			</p>
			"""
			
			send_mail(
				'New connection to your account',
				message,
				'Transcendence Team <transcendence.42lyon.project@gmail.com>',
				[user.email],
				html_message=message,
				fail_silently=True,
			)

	else:
		photo_url = response_data['image']['link']

		with urllib.request.urlopen(photo_url) as url:
			with Image.open(BytesIO(url.read())) as img:
				img_io = BytesIO()
				img.save(img_io, format='JPEG')

		isOfficial = False
		if response_data['email'] in os.environ.get('OFFICIAL_EMAILS').split(','):
			isOfficial = True

		player = Player.objects.create(currentGameID=None)
		user = CustomUser.objects.create(
			username=response_data['login'],
			email=response_data['email'],
			player=player,
			is42=True,
			isOfficial=isOfficial,
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
	
		# Send an email to the user
		if user.emailAlerts:
			message = f"""
			<p>Hello <b>{user.username}</b>,</p>
			<p>
			Welcome to transcendence! We are glad to have you with us.</br>
			Feel free to explore the platform and join the different channels to chat with other users
			and play games.
			</p>
			<p>If you received this email by mistake, please ignore it.</p>

			<p>
			Have a good day,<br>
			<i>The transcendence team</i>
			</p>
			"""
			
			send_mail(
				'Welcome to transcendence',
				message,
				'Transcendence Team <transcendence.42lyon.project@gmail.com>',
				[user.email],
				html_message=message,
				fail_silently=True,
			)
	
	return redirect('pong')


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