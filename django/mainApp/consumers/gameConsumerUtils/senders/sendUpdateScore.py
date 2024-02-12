import json

async def sendUpdateScore(consumer, gameSettings):
	for paddle in gameSettings.paddles:
		if (paddle.id < gameSettings.nbPaddles):
			if (gameSettings.isLocalGame == False):
				await consumer.channel_layer.group_send(
					f'game_{consumer.game_id}',
					{
						'type': 'update_score',
						'id': paddle.id,
						'score': paddle.score,
						'nbPaddles': gameSettings.nbPaddles,
					}
				)
			else:
				await consumer.send(json.dumps({
					'type': 'update_score',
					'id': paddle.id,
					'score': paddle.score,
					'nbPaddles': gameSettings.nbPaddles,
				}))