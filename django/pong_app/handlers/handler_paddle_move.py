import json

async def handle_paddle_move(message, consumer):
	direction = message['direction']
	step = 10;

	if (direction == 'ArrowUp'):
		if (consumer.paddle_position > 0):
			consumer.paddle_position = consumer.paddle_position - step;
		await consumer.send(json.dumps({'type': 'update_paddle_position', 'position': consumer.paddle_position}))
	elif (direction == 'ArrowDown'):
		if (consumer.paddle_position < consumer.canvas_height - 100):
			consumer.paddle_position = consumer.paddle_position + step;
		await consumer.send(json.dumps({'type': 'update_paddle_position', 'position': consumer.paddle_position}))