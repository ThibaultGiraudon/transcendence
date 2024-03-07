from django.shortcuts import render


def ranking(request, sortedBy):
	if request.method == 'GET':
		return render(request, 'base.html')
