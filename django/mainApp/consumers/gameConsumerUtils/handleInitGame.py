from 	channels.db import database_sync_to_async
from 	.classes.gameSettings import GameSettings
from	.senders.sendInitPaddlePosition import sendInitPaddlePosition
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

async def launchRankedSoloGame(consumer, gameID, gameMode):
	if gameID not in consumer.gameSettingsInstances:
		consumer.gameSettingsInstances[gameID] = GameSettings(2)

	gameSettings = consumer.gameSettingsInstances[gameID]
	await sendInitPaddlePosition(consumer, gameSettings)
	await handleBallMove(consumer, gameMode, gameSettings)

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
			await consumer.channel_layer.group_send('game', {
				'type': 'reload_page',
			})
			return (False)

	if (gameMode == 'init_ranked_solo_game'):
		await launchRankedSoloGame(consumer, gameID, gameMode)
	# elif (gameMode == 'init_death_game'):
	# 	self.launchDeathGame()
	# elif (gameMode == 'init_tournament_game'):
	# 	self.launchTournamentGame()
	return (True)