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

async def sendInitBallMessage(consumer):
	message = {
		'type': 'init_ball_position',
		'x': consumer.gameSettings.ball.x,
		'y': consumer.gameSettings.ball.y,
		'radius': consumer.gameSettings.ball.radius,
	}
	await consumer.send(json.dumps(message))

async def sendUpdateBallMessage(consumer):
	message = {
		'type': 'update_ball_position',
		'x': consumer.gameSettings.ball.x,
		'y': consumer.gameSettings.ball.y,
	}
	await consumer.send(json.dumps(message))

async def handle_ball_move(consumer):
	await sendInitPaddlePosition(consumer)
	await sendInitBallMessage(consumer)

	while (True):
		consumer.gameSettings.ball.move()

		if (consumer.gameSettings.ball.checkCollision(consumer.gameSettings.paddles[0])):
			print("Collision paddle 0")

		if (consumer.gameSettings.ball.x <= 0) or (consumer.gameSettings.ball.x >= consumer.gameSettings.gameWidth):
			consumer.gameSettings.ball.angle = math.pi - consumer.gameSettings.ball.angle

		if (consumer.gameSettings.ball.y <= 0) or (consumer.gameSettings.ball.y >= consumer.gameSettings.gameHeight):
			consumer.gameSettings.ball.angle = -consumer.gameSettings.ball.angle

		# TODO change to global var for fps
		await asyncio.sleep(0.03)
		await sendUpdateBallMessage(consumer)

async def handle_init_game(consumer):
	consumer.gameSettings.resetPaddles()
	consumer.gameSettings.ball.task = asyncio.create_task(handle_ball_move(consumer))