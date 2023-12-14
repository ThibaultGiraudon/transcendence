from    channels.generic.websocket import AsyncWebsocketConsumer
from    .handlers.handler_init_game import handle_init_game
from    .handlers.handler_paddle_move import handle_paddle_move
from    .gameObjects import *
import  json

class PongConsumer(AsyncWebsocketConsumer):
	gameSettings = GameSettings(2, 800, 800)
	gameSettings.paddles[0].x = 10
	gameSettings.paddles[1].x = gameSettings.gameWidth - gameSettings.paddles[1].width - 10

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


class NotificationConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.user = self.scope["user"]
		await self.channel_layer.group_add(
			f"notifications_{self.user.id}",
			self.channel_name
		)
		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			f"notifications_{self.user.id}",
			self.channel_name
		)
	
	async def notification_message(self, event):
		message = event['message']

		# Send message to WebSocket
		await self.send(text_data=json.dumps({
			'message': message
		}))