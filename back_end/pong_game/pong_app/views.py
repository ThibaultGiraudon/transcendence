from django.shortcuts import render
from django.db import connection

def homePage(request):
    return render(request, 'homePage.html')

def test_connection(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        connection.close()
        return render(request, 'success.html')
    except Exception as error:
        return render(request, 'error.html')