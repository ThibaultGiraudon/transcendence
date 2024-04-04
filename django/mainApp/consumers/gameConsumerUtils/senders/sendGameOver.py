from	channels.db import database_sync_to_async

@database_sync_to_async
def addStatToPlayer(playerID, paddle):
	from mainApp.models import Player, Score, Game
	player = Player.objects.get(id=playerID)

	score = Score(player=player, position=paddle.rankPosition, score=paddle.score)
	score.save()

	gameID = player.currentGameID
	game = Game.objects.get(id=gameID)
	game.scores.add(score)
	game.save()

async def sendGameOver(consumer, gameSettings, paddle):
	if (gameSettings.isLocalGame):
		playerID = gameSettings.playerIDList[0]
	else:
		playerID = gameSettings.playerIDList[paddle.id]
	if (not gameSettings.isLocalGame):
		await addStatToPlayer(playerID, paddle)
	await consumer.channel_layer.group_send(
		f'game_{gameSettings.gameID}',
		{
			'type': 'game_over',
			'gameID': gameSettings.gameID,
			'playerID': playerID,
		}
	)