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

async def launchAnyGame(consumer, gameID):
	gameSettings = consumer.gameSettingsInstances[gameID]
	await getPlayerIDList(gameSettings, gameID)
	await sendInitPaddlePosition(consumer, gameSettings)
	await sendUpdateScore(consumer, gameSettings)
	await handleBallMove(consumer, gameSettings)

async def launchRankedSoloGame(consumer, gameID):
	if gameID not in consumer.gameSettingsInstances:
		consumer.gameSettingsInstances[gameID] = GameSettings(2)
	await launchAnyGame(consumer, gameID)

async def launchDeathGame(consumer, gameID):
	if gameID not in consumer.gameSettingsInstances:
		consumer.gameSettingsInstances[gameID] = GameSettings(4)
	await launchAnyGame(consumer, gameID)

# async def launchTournamentGame(consumer, gameID):
	# if gameID not in consumer.gameSettingsInstances:
		# consumer.gameSettingsInstances[gameID] = GameSettings(4)
	# await launchAnyGame(consumer, gameID)

async def handleInitGame(consumer, gameID, gameMode, playerID):
	game = await getGame(gameID)
	if playerID not in game.playerList:
		return (False)

	player = await getPlayer(playerID)
	player.isReady = True
	await savePlayer(player)

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