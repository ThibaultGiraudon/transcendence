from django.urls import path
from .views import pongView, notificationsView, mainView, usersView, chatView, waitPlayersView

urlpatterns = [
    # Website
	path('', mainView.home, name='home'),
	path('home', mainView.home, name='home'),
	path('test/', mainView.testDBConnection, name='testDBConnection'),
	path('headerView/', mainView.headerView, name='headerView'),
    path('ken', mainView.ken, name='ken'),

	path('notifications/', notificationsView.notifications, name='notifications'),
	path('delete_notification/<int:notification_id>/', notificationsView.delete_notification, name='delete_notification'),
	path('delete_all_notifications/', notificationsView.delete_all_notifications, name='delete_all_notifications'),
    
	path('pong/', pongView.pong, name='pong'),
	path('pong/ranked/', pongView.ranked, name='ranked'),
	path('pong/practice/', pongView.practice, name='practice'),
	path('pong/game/<str:gameMode>/<str:gameID>/', pongView.game, name='game'),
	path('pong/game_over/<str:player>/', pongView.gameOver, name='game_over'),
	path('pong/wait_players/<str:gameMode>/', waitPlayersView.waitPlayers, name='wait_players'),

	path('sign_in/', usersView.sign_in, name='sign_in'),
	path('sign_up/', usersView.sign_up, name='sign_up'),
	path('sign_out/', usersView.sign_out, name='sign_out'),
	path('ft_api/', usersView.ft_api, name="ft_api"),
	path('check_authorize/', usersView.check_authorize, name="check_authorize"),
	path('profile/', usersView.profile_me, name="profile_me"),
	path('profile/<str:username>', usersView.profile, name="profile"),
	path('users/', usersView.users, name="users"),
	path('follow/<int:id>', usersView.follow, name="follow"),
	path('unfollow/<int:id>', usersView.unfollow, name="unfollow"),
	path('block/<int:id>', usersView.block, name="block"),
	path('unblock/<int:id>', usersView.unblock, name="unblock"),

	path("chat/", chatView.chat, name="chat"),
	path('create_channel/', chatView.create_channel, name='create_channel'),
	path("chat/<str:room_id>", chatView.room, name="room"),
    
	# API
	path('api/get_username/<int:id>', usersView.get_username, name="get_username"),
]