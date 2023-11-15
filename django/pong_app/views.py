from django.shortcuts import render
from django.db import connection
from pong_app.models import PongGameState

def homePage(request):
    return render(request, 'homePage.html')

def login(request):
    return render(request, 'login.html')

def pongGame(request):
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

    return render(request, 'pong_elements/index.html', {'game_state': game_state})

def testDBConnection(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        connection.close()
        return render(request, 'success.html')
    except Exception as error:
        return render(request, 'error.html')