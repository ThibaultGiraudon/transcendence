import	datetime
from	mainApp.views.utils import renderPage, redirectPage
from	mainApp.models import Game

def getNbPlayersToWait(gameMode):
	if (gameMode == 'init_ranked_solo_game'):
		return (2)
	return (4)

def createOrJoinGame(waitingGamesList, player, gameMode):
	if (waitingGamesList.exists()):
		game = waitingGamesList.first()
		game.playerList.append(player.id)
		game.save()
		return (game.id)
	newGame = Game.objects.create(
		date=datetime.date.today(),
		hour=datetime.datetime.now().time(),
		duration=0,
		gameMode=gameMode,
		playerList=[player.id]
	)
	return (newGame.id)

def waitPlayers(request, gameMode):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')

	player = request.user.player

	nbPlayersToWait = getNbPlayersToWait(gameMode)
	waitingGamesList = Game.objects\
		.filter(playerList__len__lt=nbPlayersToWait)\
		.exclude(playerList__contains=[player.id])\
		.exclude(isOver=True)\
		.filter(gameMode=gameMode)

	# If the player is already in a game and the game is not over, we redirect him to the game
	if (player.currentGameID):
		game = Game.objects.get(id=player.currentGameID)
		if (game.isOver == False):
			gameMode = game.gameMode
			if (game.playerList.__len__() == nbPlayersToWait):
				return redirectPage(request, '/pong/game/' + gameMode + '/')
			return renderPage(request, 'pong_elements/wait_players.html', {'gameMode': gameMode, 'gameID': game.id})

	gameID = createOrJoinGame(waitingGamesList, player, gameMode)
	player.currentGameID = gameID
	player.save()
	game = Game.objects.get(id=gameID)
	if (game.playerList.__len__() == nbPlayersToWait):
		return redirectPage(request, '/pong/game/' + gameMode + '/')
	return renderPage(request, 'pong_elements/wait_players.html', {'gameMode': gameMode, 'gameID': gameID})