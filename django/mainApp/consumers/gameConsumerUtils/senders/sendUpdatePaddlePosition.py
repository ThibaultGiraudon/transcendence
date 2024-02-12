import json

async def sendUpdatePaddlePosition(consumer, paddle, gameSettings):
	if (gameSettings.isLocalGame == False):
		await consumer.channel_layer.group_send(
			f'game_{consumer.game_id}',
			{
				'type': 'update_paddle_position',
				'position': paddle.position,
				'id': paddle.id,
			}
		)
	else:
		await consumer.send(json.dumps({
			'type': 'update_paddle_position',
			'position': paddle.position,
			'id': paddle.id,
		}))