from django.db import connection
from django.utils.translation import gettext as _
import random

from mainApp.views.utils import renderPage, renderError


def headerView(request):
    return renderPage(request, 'header.html')


def home(request):
	return renderPage(request, 'home.html')


def testDBConnection(request):
	try:
		with connection.cursor() as cursor:
			cursor.execute("SELECT 1")
		connection.close()
		return renderPage(request, 'success.html')
	except Exception as error:
		return renderPage(request, 'error.html')


def translate(request):
	text = _("Hello World")
	return renderPage(request, 'translate.html', {'text': text})


# Custom errors


def custom404(request, exception):
	context = {
		'title':"Page not found",
		'infos':"Please check the URL and try again."
	}

	# 1 chance to get a funny message
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