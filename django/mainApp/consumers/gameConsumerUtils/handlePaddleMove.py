import	json, asyncio

def keyupReset(direction, paddle):
	paddle.keyState[direction] = False;
	if (paddle.taskAsyncio[direction]):
		paddle.taskAsyncio[direction].cancel()

async def sendUpdatePaddleMessage(consumer, paddle):
	await consumer.channel_layer.group_send('game', {
		'type': 'update_paddle_position',
		'position': paddle.position,
		'id': paddle.id,
	})

async def keydownLoop(direction, paddle, consumer):
	if (direction == 'up'):
		paddle.keyState['down'] = False;
	elif (direction == 'down'):
		paddle.keyState['up'] = False;

	print('keydownLoop')

	while (paddle.keyState[direction] or paddle.keyState[direction]):
		if (paddle.keyState[direction] and direction == 'up' and paddle.position > 30):
			paddle.moveUp()
		elif (paddle.keyState[direction] and direction == 'down' and paddle.position < 670):
			paddle.moveDown()
		
		await sendUpdatePaddleMessage(consumer, paddle)
		await asyncio.sleep(0.01) # TODO change to global var for speed

async def handlePaddleMove(consumer, message):
	direction = message['direction']
	paddle = consumer.gameSettings.paddles[int(message['id'])]

	if (paddle.isAlive == True):
		print('handlePaddleMove')
		if (message['key'] == 'keydown'):
			if (direction == 'up'):
				paddle.keyState[direction] = True;
			elif (direction == 'down'):
				paddle.keyState[direction] = True;
			paddle.taskAsyncio[direction] = asyncio.create_task(keydownLoop(direction, paddle, consumer))

		elif (message['key'] == 'keyup'):
			keyupReset(direction, paddle)