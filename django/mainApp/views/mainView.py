from django.shortcuts import render
from django.db import connection
from django.utils.translation import gettext as _

from mainApp.views.utils import renderPage


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


def custom_404(request, exception):
	return render(request, 'errors/404.html', status=404)


def translate(request):
	text = _("Hello World")
	return renderPage(request, 'translate.html', {'text': text})