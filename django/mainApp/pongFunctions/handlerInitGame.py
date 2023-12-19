import	json
import	asyncio

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
        }
		await consumer.send(json.dumps(message))

async def sendInitScore(consumer, nbPaddles):
	for paddle in consumer.gameSettings.paddles:
		if (paddle.isAlive == False):
			continue
		# if (consumer.gameSettings.nbPaddles == 2):
			# score = paddle.score ^ 1
		# else:
		score = paddle.score
		message = {
			'type': 'init_score',
			'nbPaddles': nbPaddles,
			'score': score,
			'id': paddle.id,
		}
		await consumer.send(json.dumps(message))

async def sendUpdateBallPosition(consumer, ball):
	message = {
		'type': 'update_ball_position',
		'x': ball.x,
		'y': ball.y,
		'radius': ball.radius,
		'color': ball.color,
	}
	await consumer.send(json.dumps(message))

async def sendUpdateScore(consumer, paddleID):
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
		'nbPaddles': consumer.gameSettings.nbPaddles,
		'score': score,	
		'id': id,
	}
	await consumer.send(json.dumps(message))

async def handle_ball_move(consumer):
	await sendInitsquareSize(consumer)
	await sendInitPaddlePosition(consumer)
	await sendInitScore(consumer, consumer.gameSettings.nbPaddles)

	ball = consumer.gameSettings.ball
	while (True):
		# TODO maybe change this to bottom (ball.move)
		ball.move()

		for paddle in consumer.gameSettings.paddles:
			ball.checkPaddleCollision(paddle, consumer.gameSettings)

		paddleID = ball.checkWallCollision(consumer.gameSettings)
		paddle = consumer.gameSettings.paddles[paddleID]
		if (paddleID >= 0):
			if (paddle.score == 9):
				if (consumer.gameSettings.nbPaddles == 2):
					consumer.gameSettings.paddles[paddle.id ^ 1].isAlive = False
				else:
					paddle.isAlive = False
				paddle.color = "0x212121"
			
			await sendInitPaddlePosition(consumer)	
			await sendUpdateScore(consumer, paddleID)
			ball.resetBall(consumer.gameSettings)
			await asyncio.sleep(1)

		# TODO change to global var for fps
		await asyncio.sleep(0.01)
		await sendUpdateBallPosition(consumer, ball)

async def handle_init_game(consumer):
	consumer.gameSettings.ball.task = asyncio.create_task(handle_ball_move(consumer))