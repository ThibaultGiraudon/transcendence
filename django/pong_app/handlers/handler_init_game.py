import	json
import	asyncio
import	math

async def sendUpdateMessage(consumer):
	message = {
		'type': 'update_ball_position',
		'x': consumer.ball.x,
		'y': consumer.ball.y,
	}
	await consumer.send(json.dumps(message))

async def handle_ball_move(consumer):
	while (True):
		delta_x = consumer.ball.speed * math.cos(consumer.ball.angle)
		delta_y = consumer.ball.speed * math.sin(consumer.ball.angle)
		consumer.ball.x += delta_x
		consumer.ball.y += delta_y

		if (consumer.ball.x <= 0) or (consumer.ball.x >= consumer.gameSettings.gameWidth):
			consumer.ball.angle = math.pi - consumer.ball.angle

		if (consumer.ball.y <= 0) or (consumer.ball.y >= consumer.gameSettings.gameHeight):
			consumer.ball.angle = -consumer.ball.angle

		# TODO change to global var for fps
		await asyncio.sleep(0.03)
		await sendUpdateMessage(consumer)

async def handle_init_game(message, consumer):
	consumer.gameSettings.gameWidth = message['canvasWidth']
	consumer.gameSettings.gameHeight = message['canvasHeight']
	# consumer.paddle1.position = message['paddlePositionLeft']
	# consumer.paddle2.position = message['paddlePositionRight']
	# consumer.ball.x = message['ballPositionX']
	# consumer.ball.y = message['ballPositionY']
	consumer.ball.task = asyncio.create_task(handle_ball_move(consumer))