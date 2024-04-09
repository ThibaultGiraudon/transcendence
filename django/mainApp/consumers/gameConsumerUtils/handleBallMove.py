from	.senders.sendUpdateBallPosition import sendUpdateBallPosition
from	.senders.sendUpdateScore import sendUpdateScore	
from	.senders.sendGameOver import sendGameOver
import	asyncio

async def updateScore(consumer, gameSettings, paddleID):
	if (gameSettings.nbPaddles == 2):
		gameSettings.paddles[paddleID ^ 1].score += 1
		if (gameSettings.paddles[paddleID ^ 1].score >= 10):
			gameSettings.paddles[paddleID].isAlive = False
			gameSettings.paddles[paddleID ^ 1].isAlive = False
			gameSettings.paddles[paddleID].rankPosition = 2
			gameSettings.paddles[paddleID ^ 1].rankPosition = 1

			await sendGameOver(consumer, gameSettings, gameSettings.paddles[paddleID])
			await sendGameOver(consumer, gameSettings, gameSettings.paddles[paddleID ^ 1])
	else:
		gameSettings.paddles[paddleID].score += 1
		if (gameSettings.paddles[paddleID].score >= 10):
			gameSettings.paddles[paddleID].isAlive = False
			nbAlives = 0
			for paddle in gameSettings.paddles:
				if (paddle.isAlive):
					nbAlives += 1
			gameSettings.paddles[paddleID].rankPosition = nbAlives + 1
			await sendGameOver(consumer, gameSettings, gameSettings.paddles[paddleID])
			if (nbAlives == 1):
				for paddle in gameSettings.paddles:
					if (paddle.isAlive):
						paddle.isAlive = False
						paddle.rankPosition = 1
						paddle.score = 10
						await sendGameOver(consumer, gameSettings, paddle)

async def startBall(consumer, gameSettings):
	ball = gameSettings.ball
	while (True):
		ball.move()

		for paddle in gameSettings.paddles:
			ball.checkPaddleCollision(paddle, gameSettings)

		paddleID = ball.checkWallCollision(gameSettings)
		if (paddleID >= 0):
			await updateScore(consumer, gameSettings, paddleID)
			await sendUpdateScore(consumer, gameSettings)
			await asyncio.sleep(1)
			ball.resetBall(gameSettings)
			await asyncio.sleep(0.5)

		await asyncio.sleep(0.01)
		await sendUpdateBallPosition(consumer, gameSettings)

async def handleBallMove(consumer, gameSettings):
	if (gameSettings.ball.task):
		return
	gameSettings.ball.task = asyncio.create_task(startBall(consumer, gameSettings))