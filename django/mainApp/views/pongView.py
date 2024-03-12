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


def game(request, gameMode):
	if request.method == 'GET':
		if (request.user.is_authenticated):
			request.user.set_status("in game")
		return render(request, 'base.html')


def gameOver(request, gameID):
	if request.method == 'GET':
		return render(request, 'base.html')