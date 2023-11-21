import json
import asyncio

def keyup_reset(direction, consumer):
	if (direction == 'ArrowUp'):
		consumer.keyState[direction] = False;
	elif (direction == 'ArrowDown'):
		consumer.keyState[direction] = False;

	if (consumer.tasksAsyncio[direction]):
		consumer.tasksAsyncio[direction].cancel()

async def keydown_loop(direction, consumer):
	step = 10;

	if (direction == 'ArrowUp'):
		consumer.keyState['ArrowDown'] = False;
	elif (direction == 'ArrowDown'):
		consumer.keyState['ArrowUp'] = False;

	while (consumer.keyState[direction] or consumer.keyState[direction]):
		if (consumer.keyState[direction] and direction == 'ArrowUp' and consumer.paddle_position > 0):
			consumer.paddle_position = consumer.paddle_position - step;
		elif (consumer.keyState[direction] and direction == 'ArrowDown' and consumer.paddle_position < consumer.canvas_height - 100):
			consumer.paddle_position = consumer.paddle_position + step;

		await consumer.send(json.dumps({'type': 'update_paddle_position', 'position': consumer.paddle_position}))
		await asyncio.sleep(0.01) # TODO change to fps

async def handle_paddle_move(message, consumer):
	direction = message['direction']
	if (message['key'] == 'keydown'):
		if (direction == 'ArrowUp'):
			consumer.keyState[direction] = True;
		elif (direction == 'ArrowDown'):
			consumer.keyState[direction] = True;

		consumer.tasksAsyncio[direction] = asyncio.create_task(keydown_loop(direction, consumer))

	elif (message['key'] == 'keyup'):
		keyup_reset(direction, consumer)