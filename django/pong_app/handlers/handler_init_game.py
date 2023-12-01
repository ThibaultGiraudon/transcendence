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
            'id': paddle.id,
        }
        await consumer.send(json.dumps(message))

async def sendInitBallMessage(consumer, ball):
	message = {
		'type': 'init_ball_position',
		'x': ball.x,
		'y': ball.y,
		'radius': ball.radius,
	}
	await consumer.send(json.dumps(message))

async def sendUpdateBallMessage(consumer, ball):
	message = {
		'type': 'update_ball_position',
		'x': ball.x,
		'y': ball.y,
	}
	await consumer.send(json.dumps(message))

async def handle_ball_move(consumer):
	ball = consumer.gameSettings.ball
	await sendInitPaddlePosition(consumer)
	await sendInitBallMessage(consumer, ball)

	while (True):
		ball.move()

		if (ball.checkCollision(consumer.gameSettings.paddles[0])):
			print("Collision paddle 0")

		if (ball.x <= 0) or (ball.x >= consumer.gameSettings.gameWidth):
			ball.angle = math.pi - ball.angle

		if (ball.y <= 0) or (ball.y >= consumer.gameSettings.gameHeight):
			ball.angle = -ball.angle

		# TODO change to global var for fps
		await asyncio.sleep(0.03)
		await sendUpdateBallMessage(consumer, ball)

async def handle_init_game(consumer):
	consumer.gameSettings.resetPaddles()
	consumer.gameSettings.ball.task = asyncio.create_task(handle_ball_move(consumer))