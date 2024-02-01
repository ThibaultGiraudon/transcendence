async def sendUpdateBallPosition(consumer, ball):
	await consumer.channel_layer.group_send('game', {
		'type': 'update_ball_position',
		'x': ball.x,
		'y': ball.y,
		'color': ball.color,
	})