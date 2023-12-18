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
		message = {
			'type': 'init_score',
			'nbPaddles': nbPaddles,
			'score': paddle.score,
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
	consumer.gameSettings.paddles[paddleID].score += 1
	message = {
		'type': 'update_score',
		'nbPaddles': consumer.gameSettings.nbPaddles,
		'score': consumer.gameSettings.paddles[paddleID].score,	
		'id': consumer.gameSettings.paddles[paddleID].id,
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
		if (paddleID >= 0):
			await sendUpdateScore(consumer, paddleID)
			ball.resetBall(consumer.gameSettings)
			await asyncio.sleep(1)

		# TODO change to global var for fps
		await asyncio.sleep(0.01)
		await sendUpdateBallPosition(consumer, ball)

async def handle_init_game(consumer):
	consumer.gameSettings.ball.task = asyncio.create_task(handle_ball_move(consumer))