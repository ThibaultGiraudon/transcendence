import json
import asyncio

def keyup_reset(direction, paddle, consumer):
	if (direction == 'up'):
		consumer.keyState[paddle][direction] = False;
	elif (direction == 'down'):
		consumer.keyState[paddle][direction] = False;

	if (consumer.tasksAsyncio[paddle][direction]):
		consumer.tasksAsyncio[paddle][direction].cancel()

async def keydown_loop(direction, paddle, consumer):
	step = 10;

	if (direction == 'up'):
		consumer.keyState[paddle]['down'] = False;
	elif (direction == 'down'):
		consumer.keyState[paddle]['up'] = False;

	while (consumer.keyState[paddle][direction] or consumer.keyState[paddle][direction]):
		if (consumer.keyState[paddle][direction] and direction == 'up' and consumer.paddle_position > 0):
			consumer.paddle_position = consumer.paddle_position - step;
		elif (consumer.keyState[paddle][direction] and direction == 'down' and consumer.paddle_position < consumer.canvas_height - 100):
			consumer.paddle_position = consumer.paddle_position + step;

		await consumer.send(json.dumps({'type': 'update_paddle_position', 'position': consumer.paddle_position, 'paddle': paddle}))
		await asyncio.sleep(0.01) # TODO change to fps

async def handle_paddle_move(message, consumer):
	direction = message['direction']
	paddle = message['paddle']
	if (message['key'] == 'keydown'):
		if (direction == 'up'):
			consumer.keyState[paddle][direction] = True;
		elif (direction == 'down'):
			consumer.keyState[paddle][direction] = True;
		consumer.tasksAsyncio[paddle][direction] = asyncio.create_task(keydown_loop(direction, paddle ,consumer))

	elif (message['key'] == 'keyup'):
		keyup_reset(direction, paddle, consumer)