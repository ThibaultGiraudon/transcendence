import json
import asyncio

async def keydown_loop(direction, consumer):
	step = 10;

	while (consumer.moving):
		if (direction == 'ArrowUp' and consumer.paddle_position > 0):
			consumer.paddle_position = consumer.paddle_position - step;
			await consumer.send(json.dumps({'type': 'update_paddle_position', 'position': consumer.paddle_position}))
		elif (direction == 'ArrowDown' and consumer.paddle_position < consumer.canvas_height - 100):
			consumer.paddle_position = consumer.paddle_position + step;
			await consumer.send(json.dumps({'type': 'update_paddle_position', 'position': consumer.paddle_position}))
		await asyncio.sleep(0.02) # TODO change to fps

async def handle_paddle_move(message, consumer):
	if (message['key'] == 'keydown'):
		consumer.moving = True;
		asyncio.create_task(keydown_loop(message['direction'], consumer))
	elif (message['key'] == 'keyup'):
		consumer.moving = False;