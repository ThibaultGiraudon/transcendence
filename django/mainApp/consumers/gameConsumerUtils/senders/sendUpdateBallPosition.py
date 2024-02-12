import json

async def sendUpdateBallPosition(consumer, gameSettings):
	ball = gameSettings.ball
	if (gameSettings.isLocalGame == False):
		await consumer.channel_layer.group_send(
			f'game_{consumer.game_id}',
			{
				'type': 'update_ball_position',
				'x': ball.x,
				'y': ball.y,
				'color': ball.color,
				'radius': ball.radius,
			}
		)
	else:
		await consumer.send(json.dumps({
			'type': 'update_ball_position',
			'x': ball.x,
			'y': ball.y,
			'color': ball.color,
			'radius': ball.radius,
		}))