from django.shortcuts import render, redirect

def pong(request):
	if not request.user.is_authenticated:
		return redirect('sign_in')

	if request.method == 'GET' and 'error' in request.GET:
		return redirect('sign_in')
	return render(request, 'pong_elements/choose_mode.html')

def ranked(request):
	if not request.user.is_authenticated:
		return redirect('sign_in')

	return render(request, 'pong_elements/ranked.html')

def practice(request):
	if not request.user.is_authenticated:
		return redirect('sign_in')

	return render(request, 'pong_elements/practice.html')

def game(request, gameMode):
	if not request.user.is_authenticated:
		return redirect('sign_in')

	return render(request, 'pong_elements/pong.html', {'gameMode': gameMode})