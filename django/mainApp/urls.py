from django.urls import path
from .views import pongView, notificationsView, mainView, usersView, chatView, waitPlayersView, api

urlpatterns = [
	# Main
	path('', mainView.base, name='base'),
	path('ken/', mainView.ken, name='ken'),


	# Pages
	path('sign_in/', usersView.sign_in, name='sign_in'),
	path('sign_up/', usersView.sign_up, name='sign_up'),
	path('profile/<str:username>', usersView.profile, name="profile"),
	path('users/', usersView.users, name="users"),
	
	path('pong/', pongView.pong, name='pong'),
	
	
	# 42
	path('ft_api/', usersView.ft_api, name="ft_api"),
	path('check_authorize/', usersView.check_authorize, name="check_authorize"),
	

	# API
	path('api/is_authenticated', api.api_is_authenticated, name='api_is_authenticated'),
	path('api/sign_out', api.api_sign_out, name='api_sign_out'),
	path('api/get_user', api.api_get_user, name='api_get_user'),
	path('api/get_user/<str:username>', api.api_get_user, name='api_get_user'),
	path('api/get_username/<int:id>', api.api_get_username, name='api_get_username'),
	path('api/users', api.api_users, name='api_users'),
	path('api/follows', api.api_follows, name='api_follows'),


	# To define
	path('pong/ranked/', pongView.ranked, name='ranked'),
	path('pong/practice/', pongView.practice, name='practice'),
	path('pong/game/<str:gameMode>/<int:gameID>', pongView.game, name='game'),
	path('pong/game_over/<str:player>/', pongView.gameOver, name='game_over'),
	path('pong/wait_players/<str:gameMode>/', waitPlayersView.waitPlayers, name='wait_players'),

	path('follow/<int:id>', usersView.follow, name="follow"),
	path('unfollow/<int:id>', usersView.unfollow, name="unfollow"),
	path('block/<int:id>', usersView.block, name="block"),
	path('unblock/<int:id>', usersView.unblock, name="unblock"),

	path("chat/", chatView.chat, name="chat"),
	path('create_channel/', chatView.create_channel, name='create_channel'),
	path("chat/<str:room_id>", chatView.room, name="room"),

	path('notifications/', notificationsView.notifications, name='notifications'),
	path('delete_notification/<int:notification_id>/', notificationsView.delete_notification, name='delete_notification'),
	path('delete_all_notifications/', notificationsView.delete_all_notifications, name='delete_all_notifications'),
]