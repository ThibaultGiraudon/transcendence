import uuid
from datetime import datetime
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model, logout
from django.middleware.csrf import get_token
from django.utils import timezone

from ..models import Notification, Channel, Game, Score


# --------------------------------------------------------------------------------
# ------------------------------------ Utils -------------------------------------
# --------------------------------------------------------------------------------


def header(request):
	if not request.user.is_authenticated:
		return JsonResponse({
			'isAuthenticated': False,
		}, status=200)
	
	return JsonResponse({
		'isAuthenticated': request.user.is_authenticated,
		'username': request.user.username,
		'photo_url': request.user.photo.url,
		'nbNewNotifications': request.user.nbNewNotifications,
	}, status=200)


def generate_csrf_token(request):
	csrf_token = get_token(request)
	return JsonResponse({
		'token': csrf_token
	}, status=200)


# --------------------------------------------------------------------------------
# ---------------------------------- Get Users -----------------------------------
# --------------------------------------------------------------------------------


def isAuthenticated(request):
	if request.user.is_authenticated:
		return JsonResponse({
			'isAuthenticated': True
		}, status=200)
	
	else:
		return JsonResponse({
			'isAuthenticated': False
		}, status=200)


def get_username(request, id):
	if not request.user.is_authenticated:
		return JsonResponse({
			'username': None
		}, status=401)
	
	# Convert ID
	try:
		id = int(id)
	except ValueError:
		return JsonResponse({
			'username': None
		}, status=401)

	if id == 0:
		return JsonResponse({
			'success': False,
			'message': "You cannot interact with the system user"
		}, status=200)

	# Check if the user exist
	User = get_user_model()
	try:
		user = User.objects.get(id=id)
	except User.DoesNotExist:
		return JsonResponse({
			'username': None
		}, status=401)
	
	return JsonResponse({
		'username': user.username
	}, status=200)


def get_user(request, username=None):
	if not request.user.is_authenticated:
		return JsonResponse({
			'user': None,
			'isCurrentUser': False,
			'isAuthenticated': False
		}, status=401)
	
	index = 1

	# Get informations about the current user
	if not username or username == request.user.username or username == "me":
		channels_dict = {}
		allGames_dict = {}
		channels = list(request.user.channels.all())

		# Order by last interaction
		channels.sort(key=lambda x: x.last_interaction, reverse=True)

		for channel in channels:

			# Get users
			users_dict = {}
			for user in channel.users.all():
				users_dict[user.id] = {
					'id': user.id,
					'username': user.username,
					'photo_url': user.photo.url,
					'status': user.status,
					'followed': user.id in request.user.follows,
					'blocked': user.id in request.user.blockedUsers,
				}

			# Get last message of the channel
			last_message_obj = channel.messages.order_by('-timestamp').first()
			if last_message_obj:
				sender = last_message_obj.sender.id
				if sender == request.user.id:
					sender = request.user.username
				else:
					for user in channel.users.all():
						if user.id == int(sender):
							sender = user.username
							break

				last_message = {
					'sender': "You" if sender == request.user.username else sender,
					'message': last_message_obj.message if not last_message_obj.sender.id in request.user.blockedUsers else "This message is blocked",
					'timestamp': timezone.localtime(last_message_obj.timestamp).strftime("%d-%m-%Y %H:%M"),
				}
			else:
				last_message = None

			# Change the name of the channel if it is a private channel
			if channel.private and len(channel.users.all()) == 2:
				for user in channel.users.all():
					if user.id != request.user.id:
						channel_name = user.username
						break
			else:
				channel_name = channel.name

			# Get the creator username
			creator_username = 'No creator available'
			if channel.creator:
				if (channel.creator == request.user.id):
					creator_username = "You"
				else:
					User = get_user_model()
					try:
						user = User.objects.get(id=channel.creator)
						creator_username = user.username
					except User.DoesNotExist:
						pass

			# Add channel to the list
			channels_dict[channel.room_id] = {
				'id': channel.id,
				'room_id': channel.room_id,
				'name': channel_name,
				'private': channel.private,
				'tournament': channel.tournament,
				'users': users_dict,
				'last_message': last_message,
				'creator': channel.creator if channel.creator else None,
				'creator_username': creator_username,
				'description': channel.description if channel.description else 'No description available',
			}

		# Get all games
		game_ids = request.user.player.allGames
		games = Game.objects.filter(id__in=game_ids).order_by('-date')
		for game in games:
			players_info_dict = {}
			for player in game.playerList:
				User = get_user_model()
				user = User.objects.get(player__id=player)
				players_info_dict[user.id] = {
					'id': user.id,
					'username': user.username,
					'photo_url': user.photo.url,
				}
			
			if (game.scores.count() > 2):
				scores = game.scores.filter(player__id=request.user.player.id)
				if (scores == None):
					result = "No result"
				if (scores.first().position == 1):
					result = "1st"
				elif (scores.first().position == 2):
					result = "2nd"
				elif (scores.first().position == 3):
					result = "3rd"
				elif (scores.first().position == 4):
					result = "4th"
			else:
				try:
					scores = game.scores.filter(player__id=request.user.player.id)
					if (scores == None):
						result = "No result"
					else:
						result = str(scores.first().score) + "-"
						for player_id in game.playerList:
							if (player_id != request.user.player.id):
								scores = game.scores.filter(player__id=player_id)
								if (scores == None):
									result = "No result"
								else:
									result += str(scores.first().score)
				except:
					result = "No result"

			gameMode = game.gameMode
			game_mode = ['init_ranked_solo_game', 'init_tournament_game', 'init_death_game']
			game_title = ['Solo Game', 'Tournament Game', 'Deathmatch Game']
			
			if (game.gameMode in game_mode):
				gameMode = game_title[game_mode.index(game.gameMode)]
			allGames_dict[index] = {
				'id': game.id,
				'date': timezone.localtime(game.date).strftime("%d-%m-%Y %H:%M"),
				'duration': game.duration,
				'playersList': players_info_dict,
				'gameMode': gameMode,
				'result': result,
			}
			index += 1


		# Get player informations
		player_info = {
			'currentGameID': request.user.player.currentGameID,
			'isReady': request.user.player.isReady,
			'soloPoints': request.user.player.soloPoints,
			'deathPoints': request.user.player.deathPoints,
			'tournamentPoints': request.user.player.tournamentPoints,
			'totalPoints': request.user.player.totalPoints,
			'gamePlayed': user.player.score_set.count(),
			'allGames':	allGames_dict,
		}

		# Get informations about the user
		user_dict = {
			'id': request.user.id,
			'is42': request.user.is42,
			'isOfficial': request.user.isOfficial,
			'email': request.user.email,
			'emailAlerts': request.user.emailAlerts,
			'username': request.user.username,
			'photo_url': request.user.photo.url,
			'status': request.user.status,
			'nbNewNotifications': request.user.nbNewNotifications,
			'channels': channels_dict,
			'follows': request.user.follows,
			'friendRequests': request.user.friendRequests,
			'blockedUsers': request.user.blockedUsers,
			'favoritesChannels': request.user.favoritesChannels,
			'player': player_info,
		}

		return JsonResponse({
			'user': user_dict,
			'isCurrentUser': True,
			'isAuthenticated': True
		}, status=200)
	
	# Get informations about the user with the username
	else:

		allGames_dict = {}
		User = get_user_model()
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			return JsonResponse({'user': None})
		
		
		game_ids = user.player.allGames
		games = Game.objects.filter(id__in=game_ids).order_by('-date')
		for game in games:
			players_info_dict = {}
			for player in game.playerList:
				User = get_user_model()
				n_user = User.objects.get(player__id=player)
				players_info_dict[n_user.id] = {
					'id': n_user.id,
					'username': n_user.username,
					'photo_url': n_user.photo.url,
				}

			if (game.scores.count() > 2):
				scores = game.scores.filter(player__id=user.player.id)
				if (scores == None):
					result = "No result"
				if (scores.first().position == 1):
					result = "1st"
				elif (scores.first().position == 2):
					result = "2nd"
				elif (scores.first().position == 3):
					result = "3rd"
				elif (scores.first().position == 4):
					result = "4th"
			else:
				try:
					scores = game.scores.filter(player__id=user.player.id)
					if (scores == None):
						result = "No result"
					else:
						result = str(scores.first().score) + "-"
						for player_id in game.playerList:
							if (player_id != user.player.id):
								scores = game.scores.filter(player__id=player_id)
								if (scores == None):
									result = "No result"
								else:
									result += str(scores.first().score)
				except:
					result = "No result"

			game_mode = ['init_ranked_solo_game', 'init_tournament_game', 'init_death_game']
			game_title = ['Solo Game', 'Tournament Game', 'Deathmatch Game']
			
			if (game.gameMode in game_mode):
				gameMode = game_title[game_mode.index(game.gameMode)]

			allGames_dict[index] = {
				'id': game.id,
				'date': timezone.localtime(game.date).strftime("%d-%m-%Y %H:%M"),
				'duration': game.duration,
				'playersList': players_info_dict,
				'gameMode': gameMode,
				'result': result,
			}
			index += 1
	
		# Get player informations
		player_info = {
			'currentGameID': user.player.currentGameID,
			'isReady': user.player.isReady,
			'soloPoints': user.player.soloPoints,
			'deathPoints': user.player.deathPoints,
			'tournamentPoints': user.player.tournamentPoints,
			'totalPoints': user.player.totalPoints,
			'gamePlayed': user.player.score_set.count(),
			'allGames':	allGames_dict,
		}
		
		user_dict = {
			'id': user.id,
			'isOfficial': user.isOfficial,
			'username': user.username,
			'photo_url': user.photo.url,
			'status': user.status,
			'followed': user.id in request.user.follows,
			'blocked': user.id in request.user.blockedUsers,
			'friendRequests': user.friendRequests,
			'player': player_info,
		}

		return JsonResponse({
			'user': user_dict,
			'isCurrentUser': False
		}, status=200)


def users(request):
	if not request.user.is_authenticated:
		return JsonResponse({
			'users': None
		}, status=401)

	# Get all users exept the user with id 0
	User = get_user_model()
	users = list(User.objects.all())
	users_dict = {}
	for user in users:
		if user.id == request.user.id:
			continue
		if user.id == 0:
			continue

		users_dict[user.id] = {
			'id': user.id,
			'username': user.username,
			'photo_url': user.photo.url,
			'status': user.status,
			'followed': user.id in request.user.follows,
			'blocked': user.id in request.user.blockedUsers,
		}

	return JsonResponse({
		'users': users_dict
	}, status=200)


def change_status(request, status):
	
	if not request.user.is_authenticated:
		return JsonResponse({
			'success': False,
			'message': 'The user is not authenticated',
			'user_id': None
		}, status=200)
	
	if (request.user.player.isReady == True):
		request.user.set_status('in-game')
		return JsonResponse({
			'success': False,
			'message': 'You cannot change your status while you are ready',
			'user_id': None
		}, status=200)
	
	if (request.user.player.currentGameID):
		request.user.set_status('waiting-game')
		return JsonResponse({
			'success': False,
			'message': 'You cannot change your status while you are in a game',
			'user_id': None
		}, status=200)
	
	request.user.set_status(status)
	
	return JsonResponse({
		'success': True,
		'message': 'Status changed',
		'user_id':request.user.id
	}, status=200)


# --------------------------------------------------------------------------------
# ---------------------------------- Set Users -----------------------------------
# --------------------------------------------------------------------------------


def follow(request, id):
	if not request.user.is_authenticated:
		return JsonResponse({
			'success': False,
			'message': "The user is not authenticated"
		}, status=401)

	# Convert ID
	try:
		id = int(id)
	except ValueError:
		return JsonResponse({
			'success': False,
			'message': "Invalid id"
		}, status=401)

	if id == 0:
		return JsonResponse({
			'success': False,
			'message': "You cannot interact with the system user"
		}, status=401)

	# Check if the user exist and if he is not already followed
	User = get_user_model()
	try:
		userTo = User.objects.get(id=id)
		if id in request.user.follows:
			return JsonResponse({
				'success': False,
				'message': "User already followed"
			}, status=401)
		
		if id in request.user.blockedUsers:
			return JsonResponse({
				'success': False,
				'message': "User is blocked"
			}, status=401)
		
		if request.user.id in userTo.blockedUsers:
			return JsonResponse({
				'success': False,
				'message': "You are blocked by this user"
			}, status=401)
		
	except User.DoesNotExist:
		return JsonResponse({
			'success': False,
			'message': "User does not exist"
		}, status=401)
	
	if (request.user.id in userTo.friendRequests):
		userTo.friendRequests.remove(request.user.id)
		userTo.follows.append(request.user.id)
		userTo.save()
		request.user.follows.append(id)
		request.user.save()

		notification = Notification(user=userTo, type='accept-friend', imageType='user', imageUser=request.user.photo.url, title="New friend", message=f"{request.user.username} accepted your friend request.", redirect=f"/profile/{request.user.username}")
		notification.save()
		
		return JsonResponse({
			'success': True,
			'message': "Successful follow"
		}, status=200)
	
	request.user.friendRequests.append(id)
	request.user.save()

	# Don't send the notification if the receiver blocked the sender
	if request.user.id not in userTo.blockedUsers:
		notification = Notification(user=userTo, type='request-friend', imageType='user', userID=request.user.id, imageUser=request.user.photo.url, title="New friend request", message=f"{request.user.username} send you a friend request.", redirect=f"/profile/{request.user.username}")
		notification.save()
	
	return JsonResponse({
		'success': True,
		'message': "Successful send friend request"
	}, status=200)


def unfollow(request, id):
	if not request.user.is_authenticated:
		return JsonResponse({
			'success': False,
			'message': "The user is not authenticated"
		}, status=401)
	
	# Convert ID
	try:
		id = int(id)
	except ValueError:
		return JsonResponse({
			'success': False,
			'message': "Invalid id"
		}, status=401)
	
	if id == 0:
		return JsonResponse({
			'success': False,
			'message': "You cannot interact with the system user"
		}, status=401)
	
	# Check if the user exist and if he is followed
	User = get_user_model()
	try:
		userTo = User.objects.get(id=id)
		if id not in request.user.follows:
			return JsonResponse({
				'success': False,
				'message': "User is not followed"
			}, status=401)
		
	except User.DoesNotExist:
		return JsonResponse({
			'success': False,
			'message': "User does not exist"
		}, status=401)

	request.user.follows.remove(id)
	request.user.save()
	userTo.follows.remove(request.user.id)
	userTo.save()

	return JsonResponse({
		'success': True,
		'message': "Successful unfollow"
	}, status=200)


def block(request, id):
	if not request.user.is_authenticated:
		return JsonResponse({
			'success': False,
			'message': "The user is not authenticated"
		}, status=401)
	
	# Convert ID
	try:
		id = int(id)
	except ValueError:
		return JsonResponse({
			'success': False,
			'message': "Invalid id"
		}, status=401)
	
	if id == 0:
		return JsonResponse({
			'success': False,
			'message': "You cannot interact with the system user"
		}, status=401)

	# Check if the user exist and if he is not already blocked
	if id in request.user.blockedUsers:
		return JsonResponse({
			'success': False,
			'message': "User already blocked"
		}, status=401)
	
	# Unfollow the user if he is in the follows list
	if id in request.user.follows:
		request.user.follows.remove(id)

		User = get_user_model()
		try:
			userTo = User.objects.get(id=id)
			userTo.follows.remove(request.user.id)
			userTo.save()
		except User.DoesNotExist:
			pass
	
	if id in request.user.friendRequests:
		request.user.friendRequests.remove(id)
 
	# Block the user
	request.user.blockedUsers.append(id)
	request.user.save()

	return JsonResponse({
		'success': True,
		'message': "Successful block"
	}, status=200)


def unblock(request, id):
	if not request.user.is_authenticated:
		return JsonResponse({
			'success': False,
			'message': "The user is not authenticated"
		}, status=401)
	
	if id == 0:
		return JsonResponse({
			'success': False,
			'message': "You cannot interact with the system user"
		}, status=401)
	
	# Convert ID
	try:
		id = int(id)
	except ValueError:
		return JsonResponse({
			'success': False,
			'message': "Invalid id"
		}, status=401)
	
	# Check if the user exist and if he is blocked
	if id not in request.user.blockedUsers:
		return JsonResponse({
			'success': False,
			'message': "User not blocked"
		}, status=401)

	# Unblock the user
	request.user.blockedUsers.remove(id)
	request.user.save()

	return JsonResponse({
		'success': True,
		'message': "Successful unblock"
	}, status=200)


def sign_out(request):
	if request.user.is_authenticated:
		# Sign out the user
		request.user.set_status("offline")
		logout(request)

		return JsonResponse({
			'success': True,
			'message': "Successful sign out"
		}, status=200)
	
	else:
		return JsonResponse({
			'success': False,
			'message': "The user is not authenticated"
		}, status=401)


# --------------------------------------------------------------------------------
# ------------------------------ Get Notifications -------------------------------
# --------------------------------------------------------------------------------


def get_notifications(request):
	if not request.user.is_authenticated:
		return JsonResponse({
			'notifications': None
		}, status=401)

	# Get notifications
	notifications = list(request.user.notifications.all().order_by('-date'))
	request.user.nbNewNotifications = 0
	request.user.save()
	
	notifications_dict = {}
	for notification in notifications:
		notifications_dict[notification.id] = {
			'id': notification.id,
			'title': notification.title,
			'message': notification.message,
			'date': timezone.localtime(notification.date).strftime("%d-%m-%Y %H:%M"),
			'redirect': notification.redirect,
			'interacted': notification.interacted,
			'read': notification.read,
			'type': notification.type,
			'imageType': notification.imageType,
			'imageUser': notification.imageUser,
			'userID': notification.userID,
		}
	
	# Mark all notifications as read
	request.user.notifications.all().update(read=True)
	
	return JsonResponse({
		'notifications': notifications_dict
	}, status=200)


def interacted_notification(request, id):
	if not request.user.is_authenticated:
		return JsonResponse({
			'success': False,
			'message': "The user is not authenticated"
		}, status=401)

	# Get notification
	try:
		notification = request.user.notifications.get(id=id)
	except ObjectDoesNotExist:
		return JsonResponse({
			'success': False,
			'message': "Notification does not exist"
		}, status=401)

	# Mark the notification as interacted
	notification.interact()

	return JsonResponse({
		'success': True,
		'message': "Notification mark as interacted"
	}, status=200)


# --------------------------------------------------------------------------------
# ------------------------------ Set Notifications -------------------------------
# --------------------------------------------------------------------------------


def delete_notification(request, id):
	if not request.user.is_authenticated:
		return JsonResponse({
			'success': False,
			'message': "The user is not authenticated"
		}, status=401)

	# Get notification
	try:
		notification = request.user.notifications.get(id=id)
	except ObjectDoesNotExist:
		return JsonResponse({
			'success': False,
			'message': "Notification does not exist"
		}, status=200)

	# Delete notification
	notification.delete()

	return JsonResponse({
		'success': True,
		'message': "Notification deleted"
	}, status=200)


def delete_all_notifications(request):
	if not request.user.is_authenticated:
		return JsonResponse({
			'success': False,
			'message': "The user is not authenticated"
		}, status=401)

	# Delete all notifications
	request.user.notifications.all().delete()

	return JsonResponse({
		'success': True,
		'message': "All notifications deleted"
	}, status=200)



# --------------------------------------------------------------------------------
# -------------------------------- Get Channels ----------------------------------
# --------------------------------------------------------------------------------


def get_messages(request, room_id):
	if not request.user.is_authenticated:
		return JsonResponse({
			'messages': None
		}, status=401)

	# Get channel
	try:
		channel = request.user.channels.get(room_id=room_id)
	except ObjectDoesNotExist:
		return JsonResponse({
			'messages': None
		}, status=401)
	
	# Get messages
	messages = channel.messages.all().order_by('timestamp')
	messages_dict = {}
	
	for message in messages:
		messages_dict[message.id] = {
			'sender': message.sender.id,
			'username': message.sender.username,
			'message': message.message,
			'timestamp': message.timestamp,
		}
	
	return JsonResponse({
		'messages': messages_dict
	}, status=200)


# --------------------------------------------------------------------------------
# -------------------------------- Set Channels ----------------------------------
# --------------------------------------------------------------------------------


def create_channel(request):
	if not request.user.is_authenticated:
		return JsonResponse({
			'success': False,
			'message': 'The user is not authenticated'
		}, status=401)
	
	# Get parameters
	private = request.GET.get('private', 'False') == 'True'
	try:
		user_ids = list(map(int, request.GET.getlist('user_ids')))
	except ValueError:
		return JsonResponse({
			'success': False,
			'message': 'Invalid user_ids'
		}, status=401)

	# Create a default channel name
	channel_name = "group"
	
	# Channel informations
	room_id = str(uuid.uuid1())
	users = []

	# Get the users
	User = get_user_model()
	for user_id in user_ids:
		try:
			user = User.objects.get(id=user_id)
			users.append(user)
		except User.DoesNotExist:
			return JsonResponse({
				'success': False,
				'message': f"User {user_id} does not exist"
			}, status=401)
	
	# Check if the channel is empty
	if len(users) == 0:
		return JsonResponse({
			'success': False,
			'message': 'The channel is empty'
		}, status=401)
	
	# Check if the channel is really private
	if private and len(users) != 2:
		return JsonResponse({
			'success': False,
			'message': 'A private channel must have exactly two users'
		}, status=401)
	
	# Check if a private channel already exists between the two users
	if len(users) == 2:
		existing_channel = Channel.objects.filter(private=True, users=users[0]).filter(users=users[1])
		if existing_channel.exists():
			return JsonResponse({
				'success': False,
				'message': 'A private channel already exists between the two users'
			}, status=401)

	# Create the channel
	channel = Channel.objects.create(private=private, room_id=room_id, name=channel_name)
	channel.users.set(users)
	channel.save()

	return JsonResponse({
		'success': True,
		'message': 'Channel created',
		'room_id': room_id
	}, status=200)


def add_to_favorite(request, room_id):
	if not request.user.is_authenticated:
		return JsonResponse({
			'success': False,
			'message': "The user is not authenticated"
		}, status=401)

	# Check if the channel exist
	try:
		request.user.channels.get(room_id=room_id)
	except ObjectDoesNotExist:
		return JsonResponse({
			'success': False,
			'message': "Channel does not exist"
		}, status=401)
	
	# Check if the channel is not already in favorite
	if room_id in request.user.favoritesChannels:
		return JsonResponse({
			'success': False,
			'message': "Channel already in favorite"
		}, status=401)
	
	request.user.favoritesChannels.append(room_id)
	request.user.save()
	
	return JsonResponse({
		'success': True,
		'message': "Successful add to favorite",
		'list': request.user.favoritesChannels
	}, status=200)


def remove_from_favorite(request, room_id):
	if not request.user.is_authenticated:
		return JsonResponse({
			'success': False,
			'message': "The user is not authenticated"
		}, status=401)

	# Check if the channel exist
	try:
		request.user.channels.get(room_id=room_id)
	except ObjectDoesNotExist:
		return JsonResponse({
			'success': False,
			'message': "Channel does not exist"
		}, status=401)
	
	# Check if he is not already in favorite
	if not room_id in request.user.favoritesChannels:
		return JsonResponse({
			'success': False,
			'message': "Channel is not in favorite"
		}, status=401)
	
	request.user.favoritesChannels.remove(room_id)
	request.user.save()
	
	return JsonResponse({
		'success': True,
		'message': "Successful remove from favorite",
		'list': request.user.favoritesChannels
	}, status=200)


def add_user_to_room(request, room_id, user_id):
	if not request.user.is_authenticated:
		return JsonResponse({
			'success': False,
			'message': 'The user is not authenticated'
		}, status=401)
	
	if user_id == 0:
		return JsonResponse({
			'success': False,
			'message': 'You cannot interact with the system user'
		}, status=401)

	# Get the channel
	try:
		channel = request.user.channels.get(room_id=room_id)
	except ObjectDoesNotExist:
		return JsonResponse({
			'success': False,
			'message': 'Channel does not exist'
		}, status=401)
	
	# Get the user
	User = get_user_model()
	try:
		user = User.objects.get(id=user_id)
	except User.DoesNotExist:
		return JsonResponse({
			'success': False,
			'message': 'User does not exist'
		}, status=401)
	
	# Add the user to the channel
	channel.users.add(user)
	channel.save()

	return JsonResponse({
		'success': True,
		'message': 'User added to the channel',
		'username': user.username
	}, status=200)


def leave_channel(request, room_id):
	if not request.user.is_authenticated:
		return JsonResponse({
			'success': False,
			'message': "The user is not authenticated"
		}, status=401)
	
	# Get the channel
	try:
		channel = request.user.channels.get(room_id=room_id)
	except ObjectDoesNotExist:
		return JsonResponse({
			'success': False,
			'message': 'Channel does not exist'
		}, status=401)
	
	# Remove the channel from the favorites
	if room_id in request.user.favoritesChannels:
		request.user.favoritesChannels.remove(room_id)
		request.user.save()

	# Remove the user from the channel
	channel.users.remove(request.user)
	channel.save()

	return JsonResponse({
		'success': True,
		'message': 'User left the channel'
	}, status=200)


def create_invite_game(request, room_id):
	if not request.user.is_authenticated:
		return JsonResponse({
			'success': False,
			'message': 'User not authenticated'
		}, status=401)

	try:
		channel = request.user.channels.get(room_id=room_id)
	except ObjectDoesNotExist:
		return JsonResponse({
			'success': False,
			'message': 'Channel does not exist'
		}, status=401)

	if (len(channel.users.all()) != 2):
		return JsonResponse({
			'success': False,
			'message': 'Not enough players in the channel'
		}, status=401)

	if (request.user.player.id not in channel.users.all().values_list('player__id', flat=True)):
		return JsonResponse({
			'success': False,
			'message': 'User not in the channel'
		}, status=401)

	players = []
	for user in channel.users.all():
		players.append(user.player)
	player1 = players[0]
	player2 = players[1]

	if (request.user.player.currentGameID != None):
		return JsonResponse({
			'success': False,
			'message': 'One of the players is already in a game'
		}, status=401)

	if (request.user.player.id == player1.id):
		player2.isInvited = True
		player2.save()
		oppenent = player2
	else:
		player1.isInvited = True
		player1.save()
		oppenent = player1

	if (request.user.player.isInvited):
		gameID = oppenent.currentGameID
		request.user.player.currentGameID = gameID
		request.user.player.save()
		return JsonResponse({'success': True}, status=200)

	newGame = Game.objects.create(
		duration=0,
		gameMode='init_ranked_solo_game',
		playerList=[player1.id, player2.id],
	)
	newGame.save()

	request.user.player.currentGameID = newGame.id
	request.user.player.allGames.append(newGame.id)
	request.user.player.save()

	return JsonResponse({
		'success': True
	}, status=200)


# --------------------------------------------------------------------------------
# ---------------------------------- Get Games -----------------------------------
# --------------------------------------------------------------------------------


def get_game_info(request):
	if not request.user.is_authenticated:
		return JsonResponse({
			'success': False,
			'game_id': None,
			'player_id': None
		}, status=401)

	gameID = request.user.player.currentGameID
	if (gameID == None):
		return JsonResponse({
			'success': False,
			'game_id': None,
			'player_id': None
		}, status=200)
	
	game = Game.objects.get(id=gameID)
	if (game.gameMode == 'init_tournament_game'):
		subGame = Game.objects.get(id=game.subGames[0])
		if (not request.user.player.id in subGame.playerList):
			subGame = Game.objects.get(id=game.subGames[1])
		player = request.user.player
		player.currentGameID = subGame.id
		player.save()
		gameID = subGame.id
		game = subGame

	#Get all usernames from playerList
	players = game.playerList
	players_username = []
	players_photo = []
	for player in players:
		User = get_user_model()
		user = User.objects.get(player__id=player)
		players_username.append(user.username)
		players_photo.append(user.photo.url)

	local_game = ['init_local_game', 'init_ai_game', 'init_wall_game']
	type_game = 'online'

	if (game.gameMode in local_game):
		type_game = 'local'

	return JsonResponse({
		'success': True,
		'game_id': gameID,
		'user_id': request.user.id,
		'player_id': request.user.player.id,
		'players_username': players_username,
		'players_photo': players_photo,
		'type_game': type_game,
		'room_id': request.user.player.currentRoomID,
		'gameMode': game.gameMode
	}, status=200)


def get_game_over(request, gameID):
	if not request.user.is_authenticated:
		return JsonResponse({
			'success': False
		}, status=401)
	
	player = request.user.player
	player.currentGameID = None
	player.isReady = False
	player.save()

	game = Game.objects.get(id=gameID)
	gameMode = game.gameMode

	scores = game.scores.filter(player__id=player.id)
	if (scores == None):
		return JsonResponse({
			'success': False
		}, status=200)
	
	score = scores.first().score
	position = scores.first().position

	scoresList = []
	positionsList = []
	for scoreElement in scores:
		scoresList.append(scoreElement.score)
		positionsList.append(scoreElement.position)

	if gameMode in ['init_local_game', 'init_ai_game', 'init_wall_game']:
		game.isOver = True
		game.save()


	positionsScore = [10, 7, 3, 0]
	if (gameMode == "init_ranked_solo_game"):
		player.soloPoints.append(score + (player.soloPoints[-1] if len(player.soloPoints) > 0 else 0))
		player.totalPoints.append(score + (player.totalPoints[-1] if len(player.totalPoints) > 0 else 0))
		player.save()
	elif (gameMode == "init_death_game"):
		player.deathPoints.append(positionsScore[position - 1] + (player.deathPoints[-1] if len(player.deathPoints) > 0 else 0))
		player.totalPoints.append(positionsScore[position - 1] + (player.totalPoints[-1] if len(player.totalPoints) > 0 else 0))
		player.save()
	elif (gameMode == "init_tournament_game_sub_game"):
		return redirect_to_finals_game(game, player)
	elif (gameMode == "init_tournament_game_final_game"):
		tournamentPositionsScore = [20, 15]
		player.tournamentPoints.append(tournamentPositionsScore[position - 1] + (player.tournamentPoints[-1] if len(player.tournamentPoints) > 0 else 0))
		player.totalPoints.append(tournamentPositionsScore[position - 1] + (player.totalPoints[-1] if len(player.totalPoints) > 0 else 0))
		player.save()
		scoresList[0] = tournamentPositionsScore[position - 1]
		score = Score(player=player, position=position, score=tournamentPositionsScore[position - 1])
		score.save()
		game = Game.objects.get(id=player.allGames[-1])
		game.scores.add(score)
		game.save()
	elif (gameMode == "init_tournament_game_third_place_game"):
		tournamentPositionsScore = [7, 0]
		player.tournamentPoints.append(tournamentPositionsScore[position - 1] + (player.tournamentPoints[-1] if len(player.tournamentPoints) > 0 else 0))
		player.totalPoints.append(tournamentPositionsScore[position - 1] + (player.totalPoints[-1] if len(player.totalPoints) > 0 else 0))
		player.save()
		score = Score(player=player, position=position + 2, score=tournamentPositionsScore[position - 1])
		score.save()
		game = Game.objects.get(id=player.allGames[-1])
		game.scores.add(score)
		game.save()
		scoresList[0] = tournamentPositionsScore[position - 1]
		positionsList[0] += 2

	return JsonResponse({
		'success': True,
		'score': scoresList,
		'position': positionsList,
		'game_mode': gameMode,
		'user_id': request.user.id,
	}, status=200)


def get_ranking_points(request, sortedBy):
	if not request.user.is_authenticated:
		return JsonResponse({
			'success': False
		}, status=401)
	
	#Get all players
	User = get_user_model()
	users = User.objects.all()
	index = 0
	rank = 1
	order = None

	#split sortedBy on _ to get the sorting method and the order
	if (len(sortedBy.split('_')) == 2):
		order = sortedBy.split('_')[1]
		sortedBy = sortedBy.split('_')[0]

	#set average on users
	for user in users:
		if (len(user.player.totalPoints) > 1):
			soloPoints = user.player.soloPoints[-1]
			deathPoints = user.player.deathPoints[-1]
			tournamentPoints = user.player.tournamentPoints[-1] / 2
			totalPoints = soloPoints + deathPoints + tournamentPoints
			user.player.averagePoints = round((totalPoints / (len(user.player.totalPoints) - 1)) * 100) / 100
		else:
			user.player.averagePoints = 0
		user.save()

	if (sortedBy == 'solo'):
		sorted_users = users = sorted(users, key=lambda x: x.player.soloPoints[-1], reverse=True)
	elif (sortedBy == 'death'):
		sorted_users = sorted(users, key=lambda x: x.player.deathPoints[-1], reverse=True)
	elif (sortedBy == 'tournament'):
		sorted_users = sorted(users, key=lambda x: x.player.tournamentPoints[-1], reverse=True)
	elif (sortedBy == 'total'):
		sorted_users = sorted(users, key=lambda x: x.player.totalPoints[-1], reverse=True)
	elif (sortedBy == 'game'):
		sorted_users = sorted(users, key=lambda x: len(x.player.totalPoints), reverse=True)
	elif (sortedBy == 'average'):
		sorted_users = sorted(users, key=lambda x: x.player.averagePoints, reverse=True)
	users_dict = {}
	if (order):
		rank = len(sorted_users) - 1
		sorted_users.reverse()
	for user in sorted_users:
		if user.id == 0:
			continue

		player_dict = {
			'currentGameID': user.player.currentGameID,
			'isReady': user.player.isReady,
			'soloPoints': user.player.soloPoints,
			'deathPoints': user.player.deathPoints,
			'tournamentPoints': user.player.tournamentPoints,
			'totalPoints': user.player.totalPoints,
			'averagePoints': user.player.averagePoints,
			'gamePlayed': user.player.score_set.count(),
		}

		users_dict[index] = {
			'id': user.id,
			'username': user.username,
			'photo_url': user.photo.url,
			'status': user.status,
			'followed': user.id in request.user.follows,
			'blocked': user.id in request.user.blockedUsers,
			'player': player_dict,
			'rank': rank,
		}
		index += 1
		if (order):
			rank -= 1
		else:
			rank += 1

	return JsonResponse({
		'success': True,
		'users': users_dict
	}, status=200)


# --------------------------------------------------------------------------------
# ---------------------------------- Set Games -----------------------------------
# --------------------------------------------------------------------------------


def	quit_game(request):
	if not request.user.is_authenticated:
		return JsonResponse({
			'success': False
		}, status=401)
	
	player = request.user.player
	if (player.currentGameID != None):
		game = Game.objects.get(id=player.currentGameID)
		game.isOver = True
		game.save()

	player.currentGameID = None
	player.isReady = False
	player.save()

	return JsonResponse({
		'success': True
	}, status=200)


def	join_tournament(request):
	if not request.user.is_authenticated:
		return JsonResponse({
			'success': False,
			'message': "The user is not authenticated"
		}, status=401)
	
	# Get all tournament channels 
	channels = Channel.objects.filter(tournament=True)

	for channel in channels:
		if (channel.users.count() == 4):
			continue

		if request.user in channel.users.all():
			return JsonResponse({
				'success': False,
				'message': "User already in tournament"
			}, status=401)
		
		if len(channel.users.all()) < 4 :
			channel.users.add(request.user)
			channel.save()
			request.user.player.currentRoomID = channel.room_id
			request.user.player.save()
			if len(channel.users.all()) == 4 :
				return JsonResponse({
					'success': True,
					'message': "Tournament is full",
					'room_id': channel.room_id
				}, status=200)
			
			return JsonResponse({
				'success': True,
				'message': "User joined the tournament"
			}, status=200)
	
	room_id = str(uuid.uuid1())
	request.user.player.currentRoomID = room_id
	request.user.player.save()

	channel = Channel.objects.create(tournament=True, room_id=room_id, name='Tournament ' + datetime.now().strftime("%d-%m %H:%M"))
	channel.users.add(request.user)
	channel.save()

	return JsonResponse({
		'success': True,
		'message': "Create tournament"
	}, status=200)


def create_finals_game(game, player, isFinal):
	if (isFinal):
		gameMode = game.gameMode + "_final_game"
	else:
		gameMode = game.gameMode + "_third_place_game"
	
	newGame = Game.objects.create(
		duration=0,
		gameMode=gameMode,
		playerList=[player.id],
		parentGame=game.id,
	)
	newGame.save()

	if (isFinal):
		game.finalGame = newGame.id
	else:
		game.thirdPlaceGame = newGame.id
	game.save()
	return (newGame)


def redirect_to_finals_game(subGame, player):
	game = Game.objects.get(id=subGame.parentGame)
	scores = subGame.scores.filter(player__id=player.id)
	score = scores.first().score
	position = scores.first().position
	User = get_user_model()
	user = User.objects.get(player=player)
	message = None

	if (position == 1):
		if (game.finalGame):
			finalGame = Game.objects.get(id=game.finalGame)
			finalGame.playerList.append(player.id)
			finalGame.save()
		else:
			finalGame = create_finals_game(game, player, True)
			message = user.username + ": Get ready for the final game"
	elif (position == 2):
		if (game.thirdPlaceGame):
			finalGame = Game.objects.get(id=game.thirdPlaceGame)
			finalGame.playerList.append(player.id)
			finalGame.save()
		else:
			finalGame = create_finals_game(game, player, False)
			message = user.username + ": Get ready for the third place game"

	player.currentGameID = finalGame.id
	player.isReady = False
	player.save()

	return JsonResponse({
		'success': True,
		'redirectGameMode': finalGame.gameMode,
		'score': score,
		'position': position,
		'game_mode': game.gameMode,
		'room_id': player.currentRoomID,
		'message': message
	}, status=200)
