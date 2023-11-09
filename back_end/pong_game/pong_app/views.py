from django.shortcuts import render
from django.db import connection

def test_connection(request):
    try:
        # Tentative de connexion à la base de données
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        connection.close()
        return render(request, 'success.html')
    except Exception as e:
        # En cas d'échec de connexion, définissez un message d'erreur
        error_message = str(e)
        return render(request, 'error.html')