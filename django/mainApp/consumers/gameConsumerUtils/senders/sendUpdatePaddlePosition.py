async def sendUpdatePaddlePosition(consumer, paddle):
	await consumer.channel_layer.group_send(
		f'game_{consumer.game_id}',
		{
			'type': 'update_paddle_position',
			'position': paddle.position,
			'id': paddle.id,
		}
	)