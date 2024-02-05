async def sendInitScore(consumer, gameSettings):
	for paddle in gameSettings.paddles:
		if (paddle.isAlive == True):
			await consumer.channel_layer.group_send('game', {
				'type': 'init_score',
				'id': paddle.id,
				'score': paddle.score,
			})