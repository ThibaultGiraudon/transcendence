async def sendUpdateScore(consumer, gameSettings):
	for paddle in gameSettings.paddles:
		if (paddle.id < gameSettings.nbPaddles):
			await consumer.channel_layer.group_send(
				f'game_{consumer.game_id}',
				{
					'type': 'update_score',
					'id': paddle.id,
					'score': paddle.score,
					'nbPaddles': gameSettings.nbPaddles,
				}
			)