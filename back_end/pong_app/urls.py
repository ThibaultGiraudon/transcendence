from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
 	path('home', views.home, name='home'),
	path('pong/', views.pong, name='pong'),
	path('test/', views.testDBConnection, name='testDBConnection'),
]
