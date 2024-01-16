import	datetime
from	mainApp.views.utils import renderPage, redirectPage
from	mainApp.models import Player, Game

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

	players = Player.objects.get_or_create(username=request.user.username)
	player = players[0]

	# TODO ici changer par 2 ou 4 selon le mode de jeu
	waitingGames = Game.objects.filter(playerList__len__lt=2).exclude(playerList__contains=[player.username]).exclude(isOver=True)
	
	if (player.currentGameID):
		game = Game.objects.get(id=player.currentGameID)
		if (game.isOver == False):
			return renderPage(request, 'pong_elements/wait_players.html', {'gameMode': gameMode, 'gameID': game.id})

	if (waitingGames.exists()):
		game = waitingGames.first()
		game.playerList.append(player.username)
		game.save()
		gameID = game.id
	else:
		newGame = Game.objects.create(date=datetime.date.today(), hour=datetime.datetime.now().time(), duration=0, playerList=[player.username])
		gameID = newGame.id
		
	player.currentGameID = gameID
	player.save()
	return renderPage(request, 'pong_elements/wait_players.html', {'gameMode': gameMode, 'gameID': gameID})