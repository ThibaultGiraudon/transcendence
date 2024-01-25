from asgiref.sync import async_to_sync

def sendInitPadlePosition(consumer):
	for paddle in consumer.gameSettings.paddles:
		async_to_sync(consumer.channel_layer.group_send)('game', {
			'type': 'init_paddle_position',
			'position': paddle.position,
			'id': paddle.id,
		})