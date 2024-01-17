import	datetime
from	mainApp.views.utils import renderPage, redirectPage
from	mainApp.models import Player, Game

def getNbPlayersToWait(gameMode):
	if (gameMode == 'init_ranked_solo_game'):
		return (2)
	return (4)

def createOrJoinGame(waitingGamesList, player):
	if (waitingGamesList.exists()):
		game = waitingGamesList.first()
		game.playerList.append(player.id)
		game.save()
		return (game.id)
	newGame = Game.objects.create(date=datetime.date.today(), hour=datetime.datetime.now().time(), duration=0, playerList=[player.id])
	return (newGame.id)

def waitPlayers(request, gameMode):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')

	player = request.user.player

	nbPlayersToWait = getNbPlayersToWait(gameMode)
	waitingGamesList = Game.objects\
		.filter(playerList__len__lt=nbPlayersToWait)\
		.exclude(playerList__contains=[player.id])\
		.exclude(isOver=True)

	# If the player is already in a game and the game is not over, we redirect him to the game
	if (player.currentGameID):
		game = Game.objects.get(id=player.currentGameID)
		if (game.isOver == False):
			return renderPage(request, 'pong_elements/wait_players.html', {'gameMode': gameMode, 'gameID': game.id})

	gameID = createOrJoinGame(waitingGamesList, player)
	player.currentGameID = gameID
	player.save()
	return renderPage(request, 'pong_elements/wait_players.html', {'gameMode': gameMode, 'gameID': gameID})