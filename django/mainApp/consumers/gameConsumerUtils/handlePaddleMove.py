from 	channels.db import database_sync_to_async
from	.senders.sendUpdatePaddlePosition import sendUpdatePaddlePosition
import	asyncio, math, random

def keyupReset(direction, paddle):
	paddle.keyState[direction] = False;
	if (paddle.taskAsyncio[direction]):
		paddle.taskAsyncio[direction].cancel()

async def keydownLoop(direction, paddle, consumer, gameSettings):
	if (direction == 'up'):
		paddle.keyState['down'] = False;
	elif (direction == 'down'):
		paddle.keyState['up'] = False;

	while (paddle.keyState[direction]):
		if (direction == 'up' and paddle.position > gameSettings.limit):
			paddle.moveUp()
		elif (direction == 'down' and paddle.position < gameSettings.squareSize - gameSettings.limit - gameSettings.paddleSize):
			paddle.moveDown()
		
		await sendUpdatePaddlePosition(consumer, paddle)
		await asyncio.sleep(0.01) # TODO change to global var for speed

async def moveAiToAim(consumer, paddle, gameSettings, aimPosition):
	if (aimPosition < gameSettings.limit):
		aimPosition = gameSettings.limit
	elif (aimPosition > gameSettings.squareSize - gameSettings.paddleSize - gameSettings.limit):
		aimPosition = gameSettings.squareSize - gameSettings.paddleSize - gameSettings.limit
	while (True):
		if (aimPosition - 10 < paddle.position < aimPosition + 10):
			paddle.position = round(aimPosition)
		if (aimPosition < paddle.position):
			paddle.moveUp()
			await sendUpdatePaddlePosition(consumer, paddle)
		elif (aimPosition > paddle.position):
			paddle.moveDown()
			await sendUpdatePaddlePosition(consumer, paddle)
		await asyncio.sleep(0.01)

async def calculateAimPosition(gameSettings):
	limit = gameSettings.limit
	ball = gameSettings.ball
	angle = ball.angle
	ballX = ball.x - limit
	ballY = ball.y

	width = gameSettings.squareSize - limit * 2
	height = gameSettings.squareSize - limit

	for _ in range(5):
		angle = angle % (2 * math.pi)
		collisionYright = ballY + (width - ballX) * math.tan(angle)
		collisionYleft = ballY + (-ballX * math.tan(angle))

		if (math.pi / 2 < angle < 3 * math.pi / 2):
			if (limit < collisionYleft < height):
				return (collisionYleft)
		else:
			if (limit < collisionYright < height):
				return (collisionYright)

		collisionXtop = ballX + (0 - ballY) / math.tan(angle)
		collisionXbottom = ballX + (height - ballY) / math.tan(angle)

		if (0 < angle < math.pi):
			if (limit < collisionXbottom < width):
				ballX = collisionXbottom
				ballY = height
				angle = -angle	
		else:
			if (limit < collisionXtop < width):
				ballX = collisionXtop
				ballY = limit
				angle = -angle	

	print("CRASH AVOID\n")
	return (height)

async def aiLoop(consumer, gameSettings, paddle):
	while (True):
		collisionPosition = await calculateAimPosition(gameSettings)
		aimPosition = collisionPosition - gameSettings.paddleSize / 2 + random.randint(-10, 10)
	
		# TODO move this in class
		moveTask = asyncio.create_task(moveAiToAim(consumer, paddle, gameSettings, aimPosition))
		await asyncio.sleep(1)
		moveTask.cancel()

async def handlePaddleMove(consumer, message, gameSettings, playerID):
	direction = message['direction']
	if playerID in gameSettings.playerIDList:
		playerIndex = gameSettings.playerIDList.index(playerID)
		paddle = gameSettings.paddles[playerIndex]
	else:
		if (message['paddleKey'] in ['w', 's']):
			paddle = gameSettings.paddles[0]
		elif (message['paddleKey'] in ['o', 'l'] and not gameSettings.isAIGame):
			paddle = gameSettings.paddles[1]
		else:
			return

	aiPaddle = gameSettings.paddles[1]
	if (gameSettings.isAIGame and aiPaddle.aiTask == None):
		aiPaddle.aiTask = asyncio.create_task(aiLoop(consumer, gameSettings, aiPaddle))

	if (paddle.isAlive == True):
		if (message['key'] == 'keydown'):
			if (paddle.keyState[direction] == True):
				return
			if (direction == 'up'):
				paddle.keyState[direction] = True;
			elif (direction == 'down'):
				paddle.keyState[direction] = True;
			paddle.taskAsyncio[direction] = asyncio.create_task(keydownLoop(direction, paddle, consumer, gameSettings))

		elif (message['key'] == 'keyup'):
			keyupReset(direction, paddle)