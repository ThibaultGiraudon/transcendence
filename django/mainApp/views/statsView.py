from django.shortcuts import render


def stats(request):
	if request.method == 'GET':
		return render(request, 'base.html')
