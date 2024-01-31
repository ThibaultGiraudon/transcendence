from django.shortcuts import render


def pong(request):
	if request.method == 'GET':
		return render(request, 'base.html')


def ranked(request):
	if request.method == 'GET':
		return render(request, 'base.html')


def practice(request):
	if request.method == 'GET':
		return render(request, 'base.html')


def game(request):
	if request.method == 'GET':
		return render(request, 'base.html')


def gameOver(request, player):
	# if not request.user.is_authenticated:
	# 	return redirectPage(request, '/sign_in/')
	
	# return renderPage(request, 'pong_elements/game_over.html', {'player': player})
	pass