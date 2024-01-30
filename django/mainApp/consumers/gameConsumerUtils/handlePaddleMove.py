from	.senders.sendUpdatePaddlePosition import sendUpdatePaddlePosition
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

	while (paddle.keyState[direction] or paddle.keyState[direction]):
		if (paddle.keyState[direction] and direction == 'up' \
	  		and paddle.position > gameSettings.limit):
			paddle.moveUp()
		elif (paddle.keyState[direction] and direction == 'down' \
			and paddle.position < gameSettings.squareSize - gameSettings.limit - gameSettings.paddleSize):
			paddle.moveDown()
		
		await sendUpdatePaddlePosition(consumer, paddle)
		await asyncio.sleep(0.01) # TODO change to global var for speed

async def handlePaddleMove(consumer, message, gameSettings):
	direction = message['direction']
	paddle = gameSettings.paddles[int(message['id'])]

	if (paddle.isAlive == True):
		print('handlePaddleMove')
		if (message['key'] == 'keydown'):
			if (direction == 'up'):
				paddle.keyState[direction] = True;
			elif (direction == 'down'):
				paddle.keyState[direction] = True;
			paddle.taskAsyncio[direction] = asyncio.create_task(keydownLoop(direction, paddle, consumer, gameSettings))

		elif (message['key'] == 'keyup'):
			keyupReset(direction, paddle)