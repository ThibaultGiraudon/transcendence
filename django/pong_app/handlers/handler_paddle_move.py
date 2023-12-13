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
	ballX = ball.x
	ballY = ball.y

	while (True):
		angle = angle % (2 * math.pi)
		collisionYright = ballY + (consumer.gameSettings.gameWidth - ballX) * math.tan(angle)
		collisionYleft = ballY + (-ballX * math.tan(angle))

		if (math.pi / 2 < angle < 3 * math.pi / 2):
			if (0 < collisionYleft < consumer.gameSettings.gameHeight):
				print("left: ", collisionYleft)
		else:
			if (0 < collisionYright < consumer.gameSettings.gameHeight):
				print("right: ", collisionYright)

		collisionXbottom, collisionXtop = 0, 0
		if (angle != 0):
			collisionXbottom = ballX + (consumer.gameSettings.gameHeight - ballY) / math.tan(angle)
			collisionXtop = ballX + (-ballY / math.tan(angle))

		if (0 < angle < math.pi):
			if (0 < collisionXbottom < consumer.gameSettings.gameWidth):
				print("bottom: ", collisionXbottom)
		else:
			if (0 < collisionXtop < consumer.gameSettings.gameWidth):
				print("top: ", collisionXtop)
		


		# print("(x= ", round(collisionX), ") (y= ", round(collisionYright))
		if (0 <= collisionYright <= consumer.gameSettings.gameHeight):
			return collisionYright
		return 0
		# elif (0 <= collisionX <= consumer.gameSettings.gameWidth):
		# 	ballX = collisionX
		# 	if (collisionYright < 0):
		# 		ballY = 0
		# 	elif (collisionYright > consumer.gameSettings.gameHeight):
		# 		ballY = consumer.gameSettings.gameHeight
		# 	angle = -angle

async def aiLoop(consumer):
	paddle = consumer.ai.paddle
	while (True):
		collisionPosition = await calculateAimPosition(consumer)
		# print("collisionPosition: ", collisionPosition)

		aimPosition = collisionPosition - paddle.height / 2
		# aimPosition = 0
	
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