from    channels.generic.websocket import AsyncWebsocketConsumer
from    ..pongFunctions.handlerInitGame import handle_init_game
from    ..pongFunctions.handlerPaddleMove import handle_paddle_move
from    ..pongFunctions.gameSettingsClass import GameSettings
import  json

class PongConsumer(AsyncWebsocketConsumer):
	gameSettings = GameSettings(2, 800)

	async def connect(self):
		await self.accept()

	async def disconnect(self, close_code):
		if (self.gameSettings.ball.task):
			self.gameSettings.ball.task.cancel()

	async def receive(self, text_data):
		message = json.loads(text_data)

		if (message['type'] == 'init_game'):
			await handle_init_game(self)

		if (message['type'] == 'paddle_move'):
			await handle_paddle_move(message, self)