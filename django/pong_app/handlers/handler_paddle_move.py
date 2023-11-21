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
	direction = message['direction']
	if (message['key'] == 'keydown'):
		if (direction == 'ArrowUp'):
			consumer.moving_up = True;
			consumer.tasksAsyncio[direction] = asyncio.create_task(keydown_loop(direction, consumer))

		elif (direction == 'ArrowDown'):
			consumer.moving_down = True;
			consumer.tasksAsyncio[direction] = asyncio.create_task(keydown_loop(direction, consumer))

	elif (message['key'] == 'keyup'):
		if (direction == 'ArrowUp'):
			consumer.moving_up = False;
			if (consumer.tasksAsyncio[direction]):
				consumer.tasksAsyncio[direction].cancel()

		elif (direction == 'ArrowDown'):
			consumer.moving_down = False;
			if (consumer.tasksAsyncio[direction]):
				consumer.tasksAsyncio[direction].cancel()