from django.urls import path
from .views import pongView, notificationsView, mainView, usersView

urlpatterns = [
    path('', mainView.home, name='home'),
    path('home', mainView.home, name='home'),
    path('pong/', pongView.pong, name='pong'),
    path('notifications', notificationsView.notifications, name='notifications'),
    path('delete_notification/<int:notification_id>/', notificationsView.delete_notification, name='delete_notification'),
    path('delete_all_notifications/', notificationsView.delete_all_notifications, name='delete_all_notifications'),
    path('test/', mainView.testDBConnection, name='testDBConnection'),

    path('sign_in/', usersView.sign_in, name='sign_in'),
    path('sign_up/', usersView.sign_up, name='sign_up'),
    path('sign_out/', usersView.sign_out, name='sign_out'),
    path('ft_api/', usersView.ft_api, name="ft_api"),
    path('check_authorize/', usersView.check_authorize, name="check_authorize"),
    path('profile/', usersView.profile_me, name="profile_me"),
    path('profile/<str:username>', usersView.profile, name="profile"),
    path('users/', usersView.users, name="users"),
    path('follow/<str:username>', usersView.follow, name="follow"),
    path('unfollow/<str:username>', usersView.unfollow, name="unfollow"),
]