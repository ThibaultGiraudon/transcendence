from django.utils.translation import gettext as _
from django.shortcuts import render
import random

from mainApp.views.utils import renderError


def base(request):
	return render(request, 'base.html')


def ken(request):
	if request.method == 'GET':
		return render(request, 'base.html')


# Custom errors
def custom404(request, exception):
	context = {
		'title':"Page not found",
		'infos':"Please check the URL and try again."
	}

	# One chance to get a funny message
	if random.randint(1, 10) == 1:
		context['infos'] = "You are lost in the woods. You should have listened to your mother and stayed on the path."

	return renderError(request, 404, context)


def custom405(request, exception):
	context = {
		'title':"Method Not Allowed",
		'infos':"Please check the URL and try again."
	}
	return renderError(request, 405, context)


def custom500(request):
	context = {
		'title':"Internal Server Error",
		'infos':"Please try again later."
	}
	return renderError(request, 500, context)