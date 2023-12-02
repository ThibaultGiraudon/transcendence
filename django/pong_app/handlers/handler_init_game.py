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
	# TODO send the right score in case of ctrl+r
	message = {
		'type': 'init_score',
		'nbPaddles': nbPaddles,
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

async def sendUpdateScore(consumer, id):
	consumer.gameSettings.paddles[id].score += 1
	message = {
		'type': 'update_score',
		'nbPaddles': consumer.gameSettings.nbPaddles,
		'score': consumer.gameSettings.paddles[id].score,	
		'id': consumer.gameSettings.paddles[id].id,
	}
	await consumer.send(json.dumps(message))

async def handle_ball_move(consumer):
	ball = consumer.gameSettings.ball
	await sendInitPaddlePosition(consumer)
	await sendInitScore(consumer, consumer.gameSettings.nbPaddles)

	while (True):
		# TODO maybe change this to bottom
		ball.move()

		if (ball.checkPaddleCollision(consumer.gameSettings.paddles[0])):
			print("Collision paddle 0")

		if (ball.checkPaddleCollision(consumer.gameSettings.paddles[1])):
			print("Collision paddle 1")

		id = ball.checkWallCollision(consumer.gameSettings)
		if (id >= 0):
			await sendUpdateScore(consumer, id)

		# TODO change to global var for fps
		await asyncio.sleep(0.01)
		await sendUpdateBallMessage(consumer, ball)

async def handle_init_game(consumer):
	consumer.gameSettings.resetPaddles()
	consumer.gameSettings.ball.task = asyncio.create_task(handle_ball_move(consumer))