import json
import asyncio

def keyupReset(direction, paddle):
	if (direction == 'up'):
		paddle.keyState[direction] = False;
	elif (direction == 'down'):
		paddle.keyState[direction] = False;

	if (paddle.taskAsyncio[direction]):
		paddle.taskAsyncio[direction].cancel()

async def sendUpdateMessage(consumer, paddle):
	message = {
		'type': 'update_paddle_position',
		'position': paddle.position,
		'id': paddle.id,
	}
	await consumer.send(json.dumps(message))

async def keydownLoop(direction, paddle, consumer):
	if (direction == 'up'):
		paddle.keyState['down'] = False;
	elif (direction == 'down'):
		paddle.keyState['up'] = False;

	while (paddle.keyState[direction] or paddle.keyState[direction]):
		if (paddle.keyState[direction] and direction == 'up' and paddle.position > 0):
			paddle.position = paddle.position - paddle.speed;
		elif (paddle.keyState[direction] and direction == 'down' and paddle.position < consumer.canvasInfo['height'] - 100):
			paddle.position = paddle.position + paddle.speed;

		await sendUpdateMessage(consumer, paddle)
		await asyncio.sleep(0.03) # TODO change to global var for speed

async def handle_paddle_move(message, consumer):
	direction = message['direction']

	if (message['id'] == 'left'):
		paddle = consumer.leftPaddle
	elif (message['id'] == 'right'):
		paddle = consumer.rightPaddle

	if (message['key'] == 'keydown'):
		if (direction == 'up'):
			paddle.keyState[direction] = True;
		elif (direction == 'down'):
			paddle.keyState[direction] = True;
		paddle.taskAsyncio[direction] = asyncio.create_task(keydownLoop(direction, paddle ,consumer))

	elif (message['key'] == 'keyup'):
		keyupReset(direction, paddle)