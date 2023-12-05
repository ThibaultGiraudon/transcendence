from django.shortcuts import render, redirect
from django.db import connection
from pong_app.models import PongGameState


def home(request):
	return render(request, 'home.html')


def pong(request):
	if not request.user.is_authenticated:
		return redirect('sign_in')

	if request.method == 'GET' and 'error' in request.GET:
		return redirect('sign_in')
	return render(request, 'pong_elements/pong.html')


def testDBConnection(request):
	try:
		with connection.cursor() as cursor:
			cursor.execute("SELECT 1")
		connection.close()
		return render(request, 'success.html')
	except Exception as error:
		return render(request, 'error.html')


def custom_404(request, exception):
	return render(request, 'errors/404.html', status=404)