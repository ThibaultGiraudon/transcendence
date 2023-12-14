from django.shortcuts import render, redirect

def pong(request):
	if not request.user.is_authenticated:
		return redirect('sign_in')

	if request.method == 'GET' and 'error' in request.GET:
		return redirect('sign_in')
	return render(request, 'pong_elements/pong.html')