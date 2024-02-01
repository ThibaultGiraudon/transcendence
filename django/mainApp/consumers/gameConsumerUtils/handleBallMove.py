from	asgiref.sync import async_to_sync
from	.senders.sendUpdateBallPosition import sendUpdateBallPosition
from	.senders.sendUpdatePaddlePosition import sendUpdatePaddlePosition
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


# async def handle_ball_move(consumer, gameMode):
# 	await sendInitsquareSize(consumer)
# 	await sendInitPaddlePosition(consumer)
# 	await sendInitScore(consumer, consumer.gameSettings.nbPaddles)

# 	ball = consumer.gameSettings.ball
# 	while (True):
# 		# TODO maybe change this to bottom (ball.move)
# 		ball.move()

# 		for paddle in consumer.gameSettings.paddles:
# 			ball.checkPaddleCollision(paddle, consumer.gameSettings)

# 		paddleID = ball.checkWallCollision(consumer.gameSettings)
# 		paddle = consumer.gameSettings.paddles[paddleID]
# 		if (paddleID >= 0):
# 			if (paddle.score == 9):
# 				if (consumer.gameSettings.nbPaddles == 2):
# 					consumer.gameSettings.paddles[paddle.id ^ 1].isAlive = False
# 				else:
# 					paddle.isAlive = False
# 				paddle.color = "0x212121"
			
# 			await sendInitPaddlePosition(consumer)	
# 			await sendUpdateScore(consumer, paddleID, gameMode)
# 			ball.resetBall(consumer.gameSettings)
# 			await asyncio.sleep(1)

# 		# TODO change to global var for fps
# 		await asyncio.sleep(0.01)
# 		await sendUpdateBallPosition(consumer, ball)

async def startBall(consumer, gameSettings):
	ball = gameSettings.ball
	while (True):
		ball.move()

		for paddle in gameSettings.paddles:
			ball.checkPaddleCollision(paddle, gameSettings)

		paddleID = ball.checkWallCollision(gameSettings)
		paddle = gameSettings.paddles[paddleID]
		if (paddleID >= 0):
			# if (paddle.score == 9):
			# 	if (consumer.gameSettings.nbPaddles == 2):
			# 		consumer.gameSettings.paddles[paddle.id ^ 1].isAlive = False
			# 	else:
			# 		paddle.isAlive = False
			# 	paddle.color = "#212121"
			
			# await sendUpdateScore(consumer, paddleID, gameMode)
			for paddle in gameSettings.paddles:
				if (paddle.isAlive == True):
					paddle.position = gameSettings.squareSize / 2 - gameSettings.paddleSize / 2
					await sendUpdatePaddlePosition(consumer, paddle)
			ball.resetBall(gameSettings)
			await asyncio.sleep(1)

		await asyncio.sleep(0.02)
		await sendUpdateBallPosition(consumer, ball)

async def handleBallMove(consumer, gameMode, gameSettings):
	if (gameSettings.ball.task):
		gameSettings.ball.task.cancel()
	gameSettings.ball.task = asyncio.create_task(startBall(consumer, gameSettings))