import	uuid
from	mainApp.views.utils import renderPage, redirectPage
from	mainApp.models import Game, CustomUser

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
	print(CustomUser.objects.get(id=request.user.id).username)

	# player1 = request.user
	gameID = None

	waitingGames = Game.objects.filter(playerList__isnull=True)
	print(waitingGames)

	# if waitingGames.exists():
	# 	game = waitingGames.first()
	# 	game.playerList = [player1]
	# 	game.save()
	# 	gameID = game.id
	# else:
	# 	new_game = Game.objects.create(player_list=[player1])
	# 	gameID = new_game.id
	# return renderPage(request, 'pong_elements/wait_players.html', {'gameMode': gameMode})
	return renderPage(request, 'pong_elements/wait_players.html', {'gameMode': gameMode, 'gameID': gameID})