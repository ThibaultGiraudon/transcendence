from 	channels.db import database_sync_to_async
from 	.classes.gameSettings import GameSettings
from	.senders.sendInitPaddlePosition import sendInitPaddlePosition
from	.senders.sendUpdateScore import sendUpdateScore
from	.senders.sendReloadPage import sendReloadPage	
from 	.handleBallMove import handleBallMove

@database_sync_to_async
def getGame(gameID):
	from mainApp.models import Game
	return Game.objects.get(id=gameID)

@database_sync_to_async
def getPlayer(playerID):
	from mainApp.models import Player
	return Player.objects.get(id=playerID)

@database_sync_to_async
def savePlayer(player):
	player.save()

@database_sync_to_async
def getPlayerIDList(gameSettings, gameID):
	from mainApp.models import Game
	game = Game.objects.get(id=gameID)
	gameSettings.playerIDList = []
	for player in game.playerList:
		gameSettings.playerIDList.append(player)

@database_sync_to_async
def sendTournamentReload(consumer):
	from mainApp.models import Game
	gameID = consumer.game_id
	game = Game.objects.get(id=gameID)
	if (game.gameMode == 'init_tournament_game_sub_game'):
		parentGame = Game.objects.get(id=game.parentGame)
		return (parentGame.subGames)

async def launchAnyGame(consumer, gameID, gameMode, isLocalGame):
	if gameID not in consumer.gameSettingsInstances:
		consumer.gameSettingsInstances[gameID] = GameSettings(gameID, gameMode)
	gameSettings = consumer.gameSettingsInstances[gameID]
	gameSettings.isLocalGame = isLocalGame
	await getPlayerIDList(gameSettings, gameID)
	await sendInitPaddlePosition(consumer, gameSettings)
	await sendUpdateScore(consumer, gameSettings)
	await handleBallMove(consumer, gameSettings)

async def handleInitGame(consumer, gameID, gameMode, playerID):
	game = await getGame(gameID)
	if playerID not in game.playerList:
		return (False)

	player = await getPlayer(playerID)
	player.isReady = True
	await savePlayer(player)

	if (gameMode in [
		'init_local_game',
		'init_ai_game',
		'init_wall_game'
	]):
		await launchAnyGame(consumer, gameID, gameMode, True)
		return (True)

	for playerID in game.playerList:
		player = await getPlayer(playerID)
		if not player.isReady:
			if (gameMode == 'init_tournament_game'):
				subGamesList = await sendTournamentReload(consumer)
				for subGameID in subGamesList:
					await sendReloadPage(consumer, subGameID, playerID)
			await sendReloadPage(consumer, gameID, playerID)
			return (False)

	if (gameMode in [
		'init_ranked_solo_game', 
		'init_death_game', 
		'init_tournament_game', 
		'init_tournament_game_final_game', 
		'init_tournament_game_third_place_game'
	]):
		await launchAnyGame(consumer, gameID, gameMode, False)
	return (True)