from 	channels.db import database_sync_to_async
from 	.classes.gameSettings import GameSettings
from	.senders.sendInitPaddlePosition import sendInitPaddlePosition
from	.senders.sendUpdateScore import sendUpdateScore
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

async def launchAnyGame(consumer, gameID, isLocalGame):
	gameSettings = consumer.gameSettingsInstances[gameID]
	# gameSettings = GameSettings(gameID, 2, False)
	# consumer.gameSettingsInstances[gameID] = gameSettings
	if not isLocalGame:
		await getPlayerIDList(gameSettings, gameID)
	await sendInitPaddlePosition(consumer, gameSettings)
	await sendUpdateScore(consumer, gameSettings)
	await handleBallMove(consumer, gameSettings)

async def launchRankedSoloGame(consumer, gameID):
	if gameID not in consumer.gameSettingsInstances:
		consumer.gameSettingsInstances[gameID] = GameSettings(gameID, 2, False)
	await launchAnyGame(consumer, gameID, False)

async def launchDeathGame(consumer, gameID):
	if gameID not in consumer.gameSettingsInstances:
		consumer.gameSettingsInstances[gameID] = GameSettings(4, False)
	await launchAnyGame(consumer, gameID, False)

# async def launchTournamentGame(consumer, gameID):
	# if gameID not in consumer.gameSettingsInstances:
		# consumer.gameSettingsInstances[gameID] = GameSettings(4, False)
	# await launchAnyGame(consumer, gameID, False)

async def launchInitLocalGame(consumer, gameID):
	if gameID not in consumer.gameSettingsInstances:
		consumer.gameSettingsInstances[gameID] = GameSettings(2, False)
	await launchAnyGame(consumer, gameID, True)

async def launchInitAiGame(consumer, gameID):
	if gameID not in consumer.gameSettingsInstances:
		consumer.gameSettingsInstances[gameID] = GameSettings(2, True)
	await launchAnyGame(consumer, gameID, True)

async def launchWallGame(consumer, gameID):
	if gameID not in consumer.gameSettingsInstances:
		consumer.gameSettingsInstances[gameID] = GameSettings(1, False)
	await launchAnyGame(consumer, gameID, False)

async def handleInitGame(consumer, gameID, gameMode, playerID):
	game = await getGame(gameID)
	if playerID not in game.playerList:
		return (False)

	player = await getPlayer(playerID)
	player.isReady = True
	await savePlayer(player)

	if (gameMode == 'init_local_game'):
		await launchInitLocalGame(consumer, gameID)
		return (True)
	elif (gameMode == 'init_ai_game'):
		await launchInitAiGame(consumer, gameID)
		return (True)
	elif (gameMode == 'init_wall_game'):
		await launchWallGame(consumer, gameID)
		return (True)

	for playerID in game.playerList:
		player = await getPlayer(playerID)
		if not player.isReady:
			await consumer.channel_layer.group_send(
				f'game_{consumer.game_id}',
				{
					'type': 'reload_page',
				}
			)
			return (False)

	if (gameMode == 'init_ranked_solo_game'):
		await launchRankedSoloGame(consumer, gameID)
	elif (gameMode == 'init_death_game'):
		await launchDeathGame(consumer, gameID)
	# elif (gameMode == 'init_tournament_game'):
	# 	self.launchTournamentGame()
	return (True)