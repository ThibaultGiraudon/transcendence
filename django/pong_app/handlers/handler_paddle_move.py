import json
import asyncio
import math

def keyupReset(direction, paddle):
	if (direction == 'up'):
		paddle.keyState[direction] = False;
	elif (direction == 'down'):
		paddle.keyState[direction] = False;

	if (paddle.taskAsyncio[direction]):
		paddle.taskAsyncio[direction].cancel()

async def sendUpdatePaddleMessage(consumer, paddle):
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
			paddle.moveUp()
		elif (paddle.keyState[direction] and direction == 'down' and paddle.position < consumer.gameSettings.gameHeight - paddle.height):
			paddle.moveDown()

		await sendUpdatePaddleMessage(consumer, paddle)
		await asyncio.sleep(0.01) # TODO change to global var for speed

async def moveAiToAim(paddle, consumer, aimPosition):
	while (True):
		if (aimPosition < paddle.position):
			paddle.moveUp()
			await sendUpdatePaddleMessage(consumer, paddle)
		elif (aimPosition > paddle.position):
			paddle.moveDown()
			await sendUpdatePaddleMessage(consumer, paddle)
		await asyncio.sleep(0.01)

async def calculateAimPosition(consumer):
	ball = consumer.gameSettings.ball
	angle = ball.angle
	ball_x = ball.x
	ball_y = ball.y

	while (True):
		collisionY = ball_y + (consumer.gameSettings.gameWidth - ball_x) * math.tan(angle)
		if 0 <= collisionY <= consumer.gameSettings.gameHeight:
			return collisionY
		else:
			collisionX = abs(ball_x + (consumer.gameSettings.gameHeight - ball_y) / math.tan(angle))
			ball_x = collisionX
			angle = -angle
			# return	collisionX
			if (collisionY < 0):
				ball_y = 0
			elif (collisionY > consumer.gameSettings.gameHeight):
				ball_y = consumer.gameSettings.gameHeight
	
	# return (ball_x + (consumer.gameSettings.gameHeight - ball_y) / math.tan(angle))

async def aiLoop(consumer):
	paddle = consumer.ai.paddle
	while (True):
		collisionPosition = await calculateAimPosition(consumer)
		print("collisionPosition: ", collisionPosition)

		# aimPosition = collisionPosition - paddle.height / 2
		aimPosition = 0
	
		# TODO move this in class
		moveTask = asyncio.create_task(moveAiToAim(paddle, consumer, aimPosition))
		await asyncio.sleep(1)
		moveTask.cancel()

async def handle_paddle_move(message, consumer):
	direction = message['direction']

	if (message['id'] == '0'):
		paddle = consumer.gameSettings.paddles[0]
	elif (message['id'] == '1'):
		paddle = consumer.gameSettings.paddles[1]

	if (paddle.isAI == False):
		if (consumer.ai.task == None):
			consumer.ai.task = asyncio.create_task(aiLoop(consumer))

		if (message['key'] == 'keydown'):
			if (direction == 'up'):
				paddle.keyState[direction] = True;
			elif (direction == 'down'):
				paddle.keyState[direction] = True;
			paddle.taskAsyncio[direction] = asyncio.create_task(keydownLoop(direction, paddle, consumer))

		elif (message['key'] == 'keyup'):
			keyupReset(direction, paddle)