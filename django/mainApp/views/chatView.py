from django.shortcuts import render


def chat(request):
	if request.method == 'GET':
		return render(request, 'base.html')


def room(request, room_id):
	if request.method == 'GET':
		return render(request, 'base.html')