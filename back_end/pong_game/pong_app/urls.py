from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),   	
    path('test_connection/', views.test_connection, name='test_connection'),
]
