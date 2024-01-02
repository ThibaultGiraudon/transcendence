from django.http import JsonResponse
from mainApp.views.utils import renderPage

def pong(request):
	if not request.user.is_authenticated:
		return JsonResponse({'redirect': '/sign_in/'})

	if request.method == 'GET' and 'error' in request.GET:
		return JsonResponse({'redirect': '/sign_in/'})
	
	return renderPage(request, 'pong_elements/choose_mode.html')

def ranked(request):
	if not request.user.is_authenticated:
		return JsonResponse({'redirect': '/sign_in/'})
	
	return renderPage(request, 'pong_elements/ranked.html')

def practice(request):
	if not request.user.is_authenticated:
		return JsonResponse({'redirect': '/sign_in/'})
	
	return renderPage(request, 'pong_elements/practice.html')

def game(request, gameMode):
	if not request.user.is_authenticated:
		return JsonResponse({'redirect': '/sign_in/'})
	
	return renderPage(request, 'pong_elements/modes.html', {'gameMode': gameMode})