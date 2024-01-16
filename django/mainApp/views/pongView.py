import	datetime
from	mainApp.views.utils import renderPage, redirectPage
from	mainApp.models import Game

def pong(request):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')

	if request.method == 'GET' and 'error' in request.GET:
		return redirectPage(request, '/sign_in/')
	
	return renderPage(request, 'pong_elements/choose_mode.html')

def ranked(request):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')
	
	return renderPage(request, 'pong_elements/ranked.html')

def practice(request):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')
	
	return renderPage(request, 'pong_elements/practice.html')

def game(request, gameMode):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')
	
	return renderPage(request, 'pong_elements/modes.html', {'gameMode': gameMode})

def gameOver(request, player):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')
	
	return renderPage(request, 'pong_elements/game_over.html', {'player': player})

def waitPlayers(request, gameMode):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')

	player1 = request.user

	# TODO ici changer par 2 ou 4 selon le mode de jeu
	waitingGames = Game.objects.filter(playerList__len__lt=2).exclude(playerList__contains=[player1])
	
	if (waitingGames.exists()):
		print("game exist")
		game = waitingGames.first()
		game.playerList.append(player1)
		game.save()
		gameID = game.id
	else:
		print("pas de game")
		newGame = Game.objects.create(date=datetime.date.today(), hour=datetime.datetime.now().time(), duration=0, playerList=[player1])
		gameID = newGame.id
	return renderPage(request, 'pong_elements/wait_players.html', {'gameMode': gameMode, 'gameID': gameID})