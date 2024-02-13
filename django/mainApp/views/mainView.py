from django.utils.translation import gettext as _
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def base(request):
	return render(request, 'base.html')


def ken(request):
	if request.method == 'GET':
		return render(request, 'base.html')


def custom404(request, exception):
	return render(request, 'base.html', status=404)


def custom405(request, exception):
	return render(request, 'base.html', status=405)


def custom500(request):
	return render(request, 'base.html', status=500)


def token42(request):
	return render(request, 'base.html', status=498)


def down42(request):
	return render(request, 'base.html', status=401)