from django.shortcuts import render
from django.db import connection

def homePage(request):
    return render(request, 'homePage.html')

def pongGame(request):
    return render(request, 'pong_elements/pong_game.html')

def testDBConnection(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        connection.close()
        return render(request, 'success.html')
    except Exception as error:
        return render(request, 'error.html')