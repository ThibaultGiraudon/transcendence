from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
 	path('home', views.home, name='home'),
	path('pong/', views.pong, name='pong'),
 	path('notifications', views.notifications, name='notifications'),
	path('delete_notification/<int:notification_id>/', views.delete_notification, name='delete_notification'),
	path('delete_all_notifications/', views.delete_all_notifications, name='delete_all_notifications'),
	path('test/', views.testDBConnection, name='testDBConnection'),
]