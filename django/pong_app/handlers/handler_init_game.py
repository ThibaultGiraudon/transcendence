import	json
import	asyncio
import	math

async def sendUpdateMessage(consumer):
	message = {
		'type': 'update_ball_position',
		'x': consumer.gameSettings.ball.x,
		'y': consumer.gameSettings.ball.y,
	}
	await consumer.send(json.dumps(message))

async def handle_ball_move(consumer):
	while (True):
		delta_x = consumer.gameSettings.ball.speed * math.cos(consumer.gameSettings.ball.angle)
		delta_y = consumer.gameSettings.ball.speed * math.sin(consumer.gameSettings.ball.angle)
		consumer.gameSettings.ball.x += delta_x
		consumer.gameSettings.ball.y += delta_y

		if (consumer.gameSettings.ball.x <= 0) or (consumer.gameSettings.ball.x >= consumer.gameSettings.gameWidth):
			consumer.gameSettings.ball.angle = math.pi - consumer.gameSettings.ball.angle

		if (consumer.gameSettings.ball.y <= 0) or (consumer.gameSettings.ball.y >= consumer.gameSettings.gameHeight):
			consumer.gameSettings.ball.angle = -consumer.gameSettings.ball.angle

		# TODO change to global var for fps
		await asyncio.sleep(0.03)
		await sendUpdateMessage(consumer)

async def handle_init_game(message, consumer):
	consumer.gameSettings.gameWidth = message['canvasWidth']
	consumer.gameSettings.gameHeight = message['canvasHeight']
	consumer.gameSettings.resetPaddles()
	# consumer.paddle1.position = message['paddlePositionLeft']
	# consumer.paddle2.position = message['paddlePositionRight']
	# consumer.gameSettings.ball.x = message['ballPositionX']
	# consumer.gameSettings.ball.y = message['ballPositionY']
	message = {
		'type': 'update_paddle_position',
		'position': consumer.gameSettings.paddles[0].position,
		'id': consumer.gameSettings.paddles[0].id,
	}
	print(message)
	consumer.send(json.dumps(message))
	message = {
		'type': 'update_paddle_position',
		'position': consumer.gameSettings.paddles[1].position,
		'id': consumer.gameSettings.paddles[1].id,
	}
	print(message)
	consumer.send(json.dumps(message))
	consumer.gameSettings.ball.task = asyncio.create_task(handle_ball_move(consumer))