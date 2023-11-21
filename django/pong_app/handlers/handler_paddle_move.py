import json
import asyncio

async def keydown_loop(direction, consumer):
	step = 10;

	if (direction == 'ArrowUp'):
		consumer.moving_down = False;
	elif (direction == 'ArrowDown'):
		consumer.moving_up = False;

	while (consumer.moving_up or consumer.moving_down):
		if (consumer.moving_up and direction == 'ArrowUp' and consumer.paddle_position > 0):
			consumer.paddle_position = consumer.paddle_position - step;
		elif (consumer.moving_down and direction == 'ArrowDown' and consumer.paddle_position < consumer.canvas_height - 100):
			consumer.paddle_position = consumer.paddle_position + step;

		await consumer.send(json.dumps({'type': 'update_paddle_position', 'position': consumer.paddle_position}))
		await asyncio.sleep(0.01) # TODO change to fps

async def handle_paddle_move(message, consumer):
	if (message['key'] == 'keydown'):
		if (message['direction'] == 'ArrowUp'):
			consumer.moving_up = True;
			consumer.moving_up_task = asyncio.create_task(keydown_loop(message['direction'], consumer))

		elif (message['direction'] == 'ArrowDown'):
			consumer.moving_down = True;
			consumer.moving_down_task = asyncio.create_task(keydown_loop(message['direction'], consumer))

	elif (message['key'] == 'keyup'):
		if (message['direction'] == 'ArrowUp'):
			consumer.moving_up = False;
			if consumer.moving_up_task:
				consumer.moving_up_task.cancel()

		elif (message['direction'] == 'ArrowDown'):
			consumer.moving_down = False;
			if consumer.moving_down_task:
				consumer.moving_down_task.cancel()