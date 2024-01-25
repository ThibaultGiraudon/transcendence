from django.shortcuts import render


def pong(request):
	if request.method == 'GET':
		return render(request, 'base.html')


def ranked(request):
	# if not request.user.is_authenticated:
	# 	return redirectPage(request, '/sign_in/')
	
	# return renderPage(request, 'pong_elements/ranked.html')
	pass


def practice(request):
	# if not request.user.is_authenticated:
	# 	return redirectPage(request, '/sign_in/')
	
	# return renderPage(request, 'pong_elements/practice.html')
	pass


def game(request, gameMode, gameID):
	# if not request.user.is_authenticated:
	# 	return redirectPage(request, '/sign_in/')
	
	# return renderPage(request, 'pong_elements/modes.html', {'gameMode': gameMode, 'gameID': gameID})
	pass


def gameOver(request, player):
	# if not request.user.is_authenticated:
	# 	return redirectPage(request, '/sign_in/')
	
	# return renderPage(request, 'pong_elements/game_over.html', {'player': player})
	pass