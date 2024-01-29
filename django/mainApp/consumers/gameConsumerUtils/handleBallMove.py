from	asgiref.sync import async_to_sync
import	asyncio, json

def getUserName(id, gameMode):
	if (gameMode == 'init_local_game'):
		return 'Player ' + str(id + 1)
	if (gameMode == 'init_ai_game'):
		if (id == 0):
			return ('Player 1')
		return ('AI')
	# TODO change this to username
	return ('player')

async def sendInitsquareSize(consumer):
	message = {
		'type': 'init_game_size',
		'size': consumer.gameSettings.squareSize,
	}
	await consumer.send(json.dumps(message))

async def sendInitPaddlePosition(consumer):
	gameSettings = consumer.gameSettings
	for paddle in consumer.gameSettings.paddles:
		if (paddle.isAlive == False):
			continue
		if (paddle.id == 2 or paddle.id == 3):
			paddleThickness, paddleSize = gameSettings.paddleSize, gameSettings.paddleThickness
			offset, position = paddle.position, paddle.offset
		else:
			paddleThickness, paddleSize = gameSettings.paddleThickness, gameSettings.paddleSize
			offset, position = paddle.offset, paddle.position
		message = {
            'type': 'init_paddle_position',
			'x': offset,
            'y': position,
			'width': paddleThickness,
			'height': paddleSize,
			'color': paddle.color,
            'id': paddle.id,
			'limit': consumer.gameSettings.limit
        }
		await consumer.send(json.dumps(message))

async def sendInitScore(consumer, nbPaddles):
	for paddle in consumer.gameSettings.paddles:
		if (consumer.gameSettings.nbPaddles == 2 and paddle.id >= 2):
			continue
		score = paddle.score
		message = {
			'type': 'init_score',
			'nbPaddles': nbPaddles,
			'score': score,
			'id': paddle.id,
		}
		await consumer.send(json.dumps(message))

async def sendUpdateBallPosition(consumer, ball):
	# TODO test
	if ball.x < 0:
		ball.x = 700
	ball.x = ball.x - 20
	

	await consumer.channel_layer.group_send('game', {
		'type': 'update_ball_position',
		'x': ball.x,
		'y': ball.y,
	})

async def sendUpdateScore(consumer, paddleID, gameMode):
	if (consumer.gameSettings.nbPaddles == 2):
		consumer.gameSettings.paddles[paddleID ^ 1].score += 1
		score = consumer.gameSettings.paddles[paddleID ^ 1].score
		id = consumer.gameSettings.paddles[paddleID ^ 1].id
	else:
		consumer.gameSettings.paddles[paddleID].score += 1
		score = consumer.gameSettings.paddles[paddleID].score
		id = consumer.gameSettings.paddles[paddleID].id
	message = {
		'type': 'update_score',
		'score': score,	
		'nbPaddles': consumer.gameSettings.nbPaddles,
		'id': id,
	}
	await consumer.send(json.dumps(message))
	if (score >= 10):
		player = getUserName(id, gameMode)
		message = {
			'type': 'game_over',
			'nbPaddles': consumer.gameSettings.nbPaddles,
			'player': player,
		}
		await asyncio.sleep(1)
		await consumer.send(json.dumps(message))
		consumer.gameSettings.ball.task.cancel()

# async def handle_ball_move(consumer, gameMode):
# async def startBall(consumer, gameMode):
# 	ball = consumer.gameSettings.ball
# 	while (True):
# 		# TODO maybe change this to bottom (ball.move)
# 		ball.move()

# 		# TODO change to global var for fps
# 		await asyncio.sleep(1)
# 		await sendUpdateBallPosition(consumer, ball)

		# for paddle in consumer.gameSettings.paddles:
		# 	ball.checkPaddleCollision(paddle, consumer.gameSettings)

		# paddleID = ball.checkWallCollision(consumer.gameSettings)
		# paddle = consumer.gameSettings.paddles[paddleID]
		# if (paddleID >= 0):
		# 	if (paddle.score == 9):
		# 		if (consumer.gameSettings.nbPaddles == 2):
		# 			consumer.gameSettings.paddles[paddle.id ^ 1].isAlive = False
		# 		else:
		# 			paddle.isAlive = False
		# 		paddle.color = "0x212121"
			
		# 	await sendInitPaddlePosition(consumer)	
		# 	await sendUpdateScore(consumer, paddleID, gameMode)
		# 	ball.resetBall(consumer.gameSettings)
		# 	await asyncio.sleep(1)

		# # TODO change to global var for fps
		# await asyncio.sleep(0.01)
		# await sendUpdateBallPosition(consumer, ball)

async def startBall(consumer, gameSettings):
	ball = gameSettings.ball
	while (True):
		print('test update ball')

		await sendUpdateBallPosition(consumer, ball)
		await asyncio.sleep(1)

async def handleBallMove(consumer, gameMode, gameSettings):
	if (gameSettings.ball.task):
		gameSettings.ball.task.cancel()
	gameSettings.ball.task = asyncio.create_task(startBall(consumer, gameSettings))