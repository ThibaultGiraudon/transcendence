from	asgiref.sync import async_to_sync
from	.senders.sendUpdateBallPosition import sendUpdateBallPosition
from	.senders.sendUpdateScore import sendUpdateScore	
import	asyncio

async def updateScore(gameSettings, paddleID):
	if (gameSettings.nbPaddles == 2):
		gameSettings.paddles[paddleID ^ 1].score += 1
		if (gameSettings.paddles[paddleID ^ 1].score >= 10):
			gameSettings.paddles[paddleID].isAlive = False
	else:
		gameSettings.paddles[paddleID].score += 1
		if (gameSettings.paddles[paddleID].score >= 10):
			gameSettings.paddles[paddleID].isAlive = False

async def startBall(consumer, gameSettings):
	ball = gameSettings.ball
	while (True):
		ball.move()

		for paddle in gameSettings.paddles:
			ball.checkPaddleCollision(paddle, gameSettings)

		paddleID = ball.checkWallCollision(gameSettings)
		if (paddleID >= 0):
			await updateScore(gameSettings, paddleID)
			await sendUpdateScore(consumer, gameSettings)
			await asyncio.sleep(1)
			ball.resetBall(gameSettings)
			await asyncio.sleep(0.5)

		await asyncio.sleep(0.02)
		await sendUpdateBallPosition(consumer, gameSettings)

async def handleBallMove(consumer, gameSettings):
	if (gameSettings.ball.task):
		# TODO inutile mais a verifier quand meme si ca casse rien
		# gameSettings.ball.task.cancel()
		return
	gameSettings.ball.task = asyncio.create_task(startBall(consumer, gameSettings))