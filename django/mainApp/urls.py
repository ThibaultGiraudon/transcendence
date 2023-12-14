from django.urls import path
from .views import pongView, notificationsView, mainView

urlpatterns = [
    path('', mainView.home, name='home'),
    path('home', mainView.home, name='home'),
    path('pong/', pongView.pong, name='pong'),
    path('notifications', notificationsView.notifications, name='notifications'),
    path('delete_notification/<int:notification_id>/', notificationsView.delete_notification, name='delete_notification'),
    path('delete_all_notifications/', notificationsView.delete_all_notifications, name='delete_all_notifications'),
    path('test/', mainView.testDBConnection, name='testDBConnection'),
]