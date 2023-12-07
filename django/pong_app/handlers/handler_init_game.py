import	json
import	asyncio
import	math

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

async def sendUpdateBallMessage(consumer, ball):
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
			consumer.gameSettings.resetPaddles()
			await sendInitPaddlePosition(consumer)
			await sendUpdateScore(consumer, paddleID)

		# TODO change to global var for fps
		await asyncio.sleep(0.01)
		await sendUpdateBallMessage(consumer, ball)

async def handle_init_game(consumer):
	# TODO chamger ca pour eviter de reset les paddles a 0 a chaque ctrl + r
	consumer.gameSettings.resetPaddles()
	consumer.gameSettings.ball.task = asyncio.create_task(handle_ball_move(consumer))