from django.shortcuts import render
from django.db import connection
from django.utils.translation import gettext as _

def home(request):
	return render(request, 'home.html')

def testDBConnection(request):
	try:
		with connection.cursor() as cursor:
			cursor.execute("SELECT 1")
		connection.close()
		return render(request, 'success.html')
	except Exception as error:
		return render(request, 'error.html')

def custom_404(request, exception):
	return render(request, 'errors/404.html', status=404)

def translate(request):
	text = _("Hello World")
	return render(request, 'translate.html', {'text': text})