async def sendInitPaddlePosition(consumer, gameSettings):
	for paddle in gameSettings.paddles:
		if (paddle.isAlive == True):
			await consumer.channel_layer.group_send(
				f'game_{consumer.game_id}',
				{
					'type': 'init_paddle_position',
					'position': paddle.position,
					'id': paddle.id,
				}
			)