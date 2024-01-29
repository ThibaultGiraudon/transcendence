async def sendInitPadlePosition(consumer):
	for paddle in consumer.gameSettings.paddles:
		await consumer.channel_layer.group_send('game', {
			'type': 'init_paddle_position',
			'position': paddle.position,
			'id': paddle.id,
		})	