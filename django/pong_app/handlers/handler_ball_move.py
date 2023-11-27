import	json
import	asyncio
import	math

async def sendUpdateMessage(consumer):
	message = {
		'type': 'update_ball_position',
		'position': consumer.ballPosition,
	}
	await consumer.send(json.dumps(message))

async def handle_ball_move(consumer):
	while (True):
		delta_x = consumer.ballPosition['speed'] * math.cos(consumer.ballPosition['angle'])
		delta_y = consumer.ballPosition['speed'] * math.sin(consumer.ballPosition['angle'])
		consumer.ballPosition['x'] += delta_x
		consumer.ballPosition['y'] += delta_y

		if (consumer.ballPosition['x'] <= 0) or (consumer.ballPosition['x'] >= consumer.canvasInfo['width']):
			consumer.ballPosition['angle'] = math.pi - consumer.ballPosition['angle']

		if (consumer.ballPosition['y'] <= 0) or (consumer.ballPosition['y'] >= consumer.canvasInfo['height']):
			consumer.ballPosition['angle'] = -consumer.ballPosition['angle']

		await asyncio.sleep(0.03)
		await sendUpdateMessage(consumer)