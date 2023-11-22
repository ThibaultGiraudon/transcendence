import json

async def handle_init_game(message, consumer):
	consumer.canvasInfo['width'] = message['canvas_width']
	consumer.canvasInfo['height'] = message['canvas_height']