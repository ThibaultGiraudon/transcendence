import	json

async def handle_ball_move(message, consumer):
	print(message)
	consumer.ballPosition['x'] += 100;
	consumer.ballPosition['y'] += 100;
	message = {
		'type': 'update_ball_position',
		'position': consumer.ballPosition,
	}
	await consumer.send(json.dumps(message))