from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('login/', views.login, name='login'),
    path('pong/', views.pongGame, name='pong'),
    path('test/', views.testDBConnection, name='testDBConnection'),
]
