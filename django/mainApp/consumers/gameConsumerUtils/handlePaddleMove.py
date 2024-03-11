from 	channels.db import database_sync_to_async
from	.senders.sendUpdatePaddlePosition import sendUpdatePaddlePosition
from	.handleAIMove import aiLoop
import	asyncio

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
		await asyncio.sleep(0.01)

async def handlePaddleMove(consumer, message, gameSettings, playerID):
	direction = message['direction']
	if (gameSettings.isLocalGame):
		if (message['paddleKey'] in ['w', 's']):
			paddle = gameSettings.paddles[0]
		elif (message['paddleKey'] in ['o', 'l'] and not gameSettings.isAIGame):
			paddle = gameSettings.paddles[1]
		else:
			return
	else:
		playerIndex = gameSettings.playerIDList.index(playerID)
		paddle = gameSettings.paddles[playerIndex]

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