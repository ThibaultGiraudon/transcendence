import json

async def handle_init_game(message, consumer):
	consumer.canvas_width = message['canvas_width']
	consumer.canvas_height = message['canvas_height']
	consumer.paddle_position = consumer.canvas_height / 2
	await consumer.send(json.dumps({'type': 'update_paddle_position', 'position': consumer.paddle_position}))