import json
import asyncio
import math
import random

def keyupReset(direction, paddle):
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
		if (paddle.keyState[direction] and direction == 'up' and paddle.position > consumer.gameSettings.limit):
			paddle.moveUp()
		elif (paddle.keyState[direction] and direction == 'down' and paddle.position < consumer.gameSettings.squareSize - paddle.size - consumer.gameSettings.limit):
			paddle.moveDown()
		
		await sendUpdatePaddleMessage(consumer, paddle)
		await asyncio.sleep(0.01) # TODO change to global var for speed

async def moveAiToAim(paddle, consumer, aimPosition):
	while (True):
		if (aimPosition - 10 < paddle.position < aimPosition + 10):
			paddle.position = round(aimPosition)
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
	ballX = ball.x - 30
	ballY = ball.y

	width = consumer.gameSettings.squareSize - 60
	height = consumer.gameSettings.squareSize

	for _ in range(5):
		angle = angle % (2 * math.pi)
		collisionYright = ballY + (width - ballX) * math.tan(angle)
		collisionYleft = ballY + (-ballX * math.tan(angle))

		if (math.pi / 2 < angle < 3 * math.pi / 2):
			if (0 < collisionYleft < height):
				return (collisionYleft)
		else:
			if (0 < collisionYright < height):
				return (collisionYright)

		collisionXtop = ballX + (0 - ballY) / math.tan(angle)
		collisionXbottom = ballX + (height - ballY) / math.tan(angle)

		if (0 < angle < math.pi):
			if (30 < collisionXbottom < width):
				ballX = collisionXbottom
				ballY = height
				angle = -angle	
		else:
			if (30 < collisionXtop < width):
				ballX = collisionXtop
				ballY = 0
				angle = -angle	

	print("x=", ballX, "y=", ballY, "angle=", angle)	
	print("collisionXtop=", collisionXtop, "collisionXbottom=", collisionXbottom)
	print("collisionYright=", collisionYright, "collisionYleft=", collisionYleft)
	print("CRASH AVOID\n")
	return (height)

async def aiLoop(consumer, paddle):
	while (True):
		collisionPosition = await calculateAimPosition(consumer)

		# TODO
		# aimPosition = collisionPosition - paddle.size / 2
		aimPosition = collisionPosition - paddle.size / 2 + random.randint(-20, 20)
	
		# TODO move this in class
		moveTask = asyncio.create_task(moveAiToAim(paddle, consumer, aimPosition))
		await asyncio.sleep(1)
		moveTask.cancel()

async def handle_paddle_move(message, consumer):
	direction = message['direction']
	paddle = consumer.gameSettings.paddles[int(message['id'])]

	# TODO
	# for paddle in consumer.gameSettings.paddles:
	# 	if (paddle.aiTask == None):
	# 		paddle.aiTask = asyncio.create_task(aiLoop(consumer, paddle))

	if (paddle.isAI == False):
		if (message['key'] == 'keydown'):
			if (direction == 'up'):
				paddle.keyState[direction] = True;
			elif (direction == 'down'):
				paddle.keyState[direction] = True;
			paddle.taskAsyncio[direction] = asyncio.create_task(keydownLoop(direction, paddle, consumer))

		elif (message['key'] == 'keyup'):
			keyupReset(direction, paddle)