async def sendInitPadlePosition(consumer, gameSettings):
	for paddle in gameSettings.paddles:
		await consumer.channel_layer.group_send('game', {
			'type': 'init_paddle_position',
			'position': paddle.position,
			'id': paddle.id,
		})