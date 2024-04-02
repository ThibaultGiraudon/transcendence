from	mainApp.models import Game
from	django.http import JsonResponse
from	django.shortcuts import render
import	datetime, json

def getNbPlayersToWait(gameMode):
	if gameMode in [
		'init_local_game',
		'init_ai_game',
		'init_wall_game'
	]:
		return (1)
	if (gameMode in [
		'init_ranked_solo_game',
		'init_tournament_game_final_game', 
		'init_tournament_game_third_place_game'
	]):
		return (2)
	return (4)

def joinTournamentGame(game, player, gameMode):
	subGame = Game.objects.get(id=game.subGames[0])
	if (subGame.playerList.__len__() == 2):
		if (game.subGames.__len__() == 1):
			newSubGame = Game.objects.create(
				duration=0,
				gameMode=gameMode + '_sub_game',
				playerList=[],
				parentGame=game.id,
			)
			game.subGames.append(newSubGame.id)
			game.save()

		subGame = Game.objects.get(id=game.subGames[1])

	subGame.playerList.append(player.id)
	subGame.save()

def createGame(player, gameMode):
	newSubGameID = None
	if (gameMode == 'init_tournament_game'):
		newSubGame = Game.objects.create(
									duration=0,
									gameMode=gameMode + '_sub_game',
									playerList=[player.id],
								)
		newSubGameID = newSubGame.id

	newGame = Game.objects.create(
								duration=0,
								gameMode=gameMode,
								playerList=[player.id],
								subGames=[newSubGameID],
							)
	if (gameMode == 'init_tournament_game'):
		newSubGame.parentGame = newGame.id
		newSubGame.save()
	return (newGame.id)

def createOrJoinGame(waitingGamesList, player, gameMode):
	if (waitingGamesList.exists()):
		game = waitingGamesList.first()
		if (game.gameMode == 'init_tournament_game'):
			joinTournamentGame(game, player, gameMode)

		game.playerList.append(player.id)
		game.save()
		return (game.id)
	return (createGame(player, gameMode))

def returnJsonResponse(game, nbPlayersToWait, gameMode, playerID):
	gameID = game.id
	if (game.playerList.__len__() == nbPlayersToWait):
		if (gameMode == 'init_tournament_game'):
			subGame = Game.objects.get(id=game.subGames[0])
			if (not playerID in subGame.playerList):
				subGame = Game.objects.get(id=game.subGames[1])
			gameID = subGame.id
		return JsonResponse({'success': True, 'redirect': '/pong/game/', 'gameMode': gameMode, 'gameID': gameID})
	if (gameMode == 'init_tournament_game_sub_game'):
		gameMode = 'init_tournament_game'
	return JsonResponse({'success': True, 'redirect': '/pong/wait_players/', 'gameMode': gameMode, 'gameID': gameID})

def waitPlayers(request, gameMode):
	if (request.method == 'GET'):
		return render(request, 'base.html')
	elif (request.method == 'POST'):
		data = json.loads(request.body)
		gameMode = data.get('gameMode')
		player = request.user.player

		nbPlayersToWait = getNbPlayersToWait(gameMode)

		# If the player is already in a game and the game is not over, we redirect him to the game
		if (player.currentGameID):
			game = Game.objects.get(id=player.currentGameID)
			if (game.isOver == False):
				if (game.parentGame != None and gameMode == 'init_tournament_game_sub_game'):
					game = Game.objects.get(id=game.parentGame)
				return returnJsonResponse(game, getNbPlayersToWait(game.gameMode), game.gameMode, request.user.player.id)

		waitingGamesList = Game.objects\
			.filter(playerList__len__lt=nbPlayersToWait)\
			.exclude(playerList__contains=[player.id])\
			.exclude(isOver=True)\
			.exclude(isPrivate=True)\
			.filter(gameMode=gameMode)
		
		gameID = createOrJoinGame(waitingGamesList, player, gameMode)
		player.currentGameID = gameID
		if (gameMode not in [
			'init_local_game',
			'init_ai_game',
			'init_wall_game'
		]):
			player.allGames.append(gameID)
		player.save()
		game = Game.objects.get(id=gameID)
		return returnJsonResponse(game, nbPlayersToWait, gameMode, request.user.player.id)
	else:
		return JsonResponse({'success': False, 'message': 'Method not allowed'})