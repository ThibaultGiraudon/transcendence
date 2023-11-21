import json
import asyncio

async def keydown_loop(direction, consumer):
	step = 10;

	if (direction == 'ArrowUp'):
		consumer.moving_down = False;
	elif (direction == 'ArrowDown'):
		consumer.moving_up = False;
	print(f"keydown_loop moving_up: {consumer.moving_up}")
	print(f"keydown_loop moving_down: {consumer.moving_down}")

	while (consumer.moving_up or consumer.moving_down):
		if (consumer.moving_up and direction == 'ArrowUp' and consumer.paddle_position > 0):
			consumer.paddle_position = consumer.paddle_position - step;
		elif (consumer.moving_down and direction == 'ArrowDown' and consumer.paddle_position < consumer.canvas_height - 100):
			consumer.paddle_position = consumer.paddle_position + step;

		await consumer.send(json.dumps({'type': 'update_paddle_position', 'position': consumer.paddle_position}))
		await asyncio.sleep(0.02) # TODO change to fps

async def handle_paddle_move(message, consumer):
	if (message['key'] == 'keydown'):
		if (message['direction'] == 'ArrowUp'):
			consumer.moving_up = True;
		elif (message['direction'] == 'ArrowDown'):
			consumer.moving_down = True;
		asyncio.create_task(keydown_loop(message['direction'], consumer))
		#             consumer.moving_down_task = asyncio.create_task(move_paddle(consumer, 'ArrowDown'))
	elif (message['key'] == 'keyup'):
		if (message['direction'] == 'ArrowUp'):
			consumer.moving_up = False;
		elif (message['direction'] == 'ArrowDown'):
			consumer.moving_down = False;