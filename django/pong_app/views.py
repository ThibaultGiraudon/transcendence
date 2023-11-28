from django.shortcuts import render, redirect
from django.db import connection
from pong_app.models import PongGameState

def home(request):
	return render(request, 'home.html')

def pong(request):
	# Check if the user is already connected
	if not request.user.is_authenticated:
		return redirect('sign_in')

	# Check arguments
	if request.method == 'GET' and 'error' in request.GET:
		return redirect('sign_in')
	
	game_state, created = PongGameState.objects.get_or_create(pk=1)

	# Traitez les événements ou la logique du jeu ici
	# Pour cet exemple, nous utilisons simplement la position de la raquette
	if request.method == 'POST':
		if 'up' in request.POST and game_state.paddle_position > 0:
			game_state.paddle_position -= 10
		elif 'down' in request.POST and game_state.paddle_position < 500:
			game_state.paddle_position += 10

		# Enregistrez la nouvelle position de la raquette dans la base de données
		game_state.save()

	return render(request, 'pong_elements/pong.html', {'game_state': game_state})

def testDBConnection(request):
	try:
		with connection.cursor() as cursor:
			cursor.execute("SELECT 1")
		connection.close()
		return render(request, 'success.html')
	except Exception as error:
		return render(request, 'error.html')
