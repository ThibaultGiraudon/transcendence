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
		request.user.set_status("in game")
		return render(request, 'base.html')


def gameOver(request, gameMode):
	# if request.method == 'GET':
	# 	request.user.set_status("online")
	# 	return render(request, 'base.html')
	pass