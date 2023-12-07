import	json
import	asyncio

async def sendInitPaddlePosition(consumer):
    for paddle in consumer.gameSettings.paddles:
        message = {
            'type': 'init_paddle_position',
			'x': paddle.x,
            'y': paddle.y,
			'width': paddle.width,
			'height': paddle.height,
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
	ball = consumer.gameSettings.ball
	await sendInitPaddlePosition(consumer)
	await sendInitScore(consumer, consumer.gameSettings.nbPaddles)

	while (True):
		# TODO maybe change this to bottom (ball.move)
		ball.move()

		for paddle in consumer.gameSettings.paddles:
			ball.checkPaddleCollision(paddle)

		paddleID = ball.checkWallCollision(consumer.gameSettings)
		if (paddleID >= 0):
			await sendUpdateScore(consumer, paddleID)
			ball.resetBall(consumer.gameSettings)
			await asyncio.sleep(1)

		# TODO change to global var for fps
		await asyncio.sleep(0.01)
		await sendUpdateBallPosition(consumer, ball)

async def handle_init_game(consumer):
	consumer.gameSettings.ball.resetBall(consumer.gameSettings)
	consumer.gameSettings.ball.task = asyncio.create_task(handle_ball_move(consumer))