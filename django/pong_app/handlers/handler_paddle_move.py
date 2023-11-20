import json

async def handle_paddle_move(message, consumer):
	direction = message['direction']
	if (direction == 'ArrowUp'):
		position = 0
		await consumer.send(json.dumps({'type': 'update_paddle_position', 'position': position}))
	elif (direction == 'ArrowDown'):
		position = 400
		await consumer.send(json.dumps({'type': 'update_paddle_position', 'position': position}))