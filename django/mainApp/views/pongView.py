from	mainApp.views.utils import renderPage, redirectPage

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

def game(request, gameMode, gameID):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')
	
	return renderPage(request, 'pong_elements/modes.html', {'gameMode': gameMode, 'gameID': gameID})

def gameOver(request, player):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')
	
	return renderPage(request, 'pong_elements/game_over.html', {'player': player})