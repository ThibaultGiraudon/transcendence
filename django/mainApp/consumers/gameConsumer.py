from    channels.generic.websocket import AsyncWebsocketConsumer
from    ..pongFunctions.handlerInitGame import handle_init_game
from    ..pongFunctions.handlerPaddleMove import handle_paddle_move
from    ..pongFunctions.gameSettingsClass import GameSettings
import  json

class GameConsumer(AsyncWebsocketConsumer):
	gameSettings = GameSettings(800)

	async def connect(self):
		await self.channel_layer.group_add('game', self.channel_name)
		await self.accept()

	async def disconnect(self, close_code):
		# if (self.gameSettings.ball.task):
			# self.gameSettings.ball.task.cancel()
		await self.channel_layer.group_discard('game', self.channel_name)

	async def receive(self, text_data):
		message = json.loads(text_data)
		print(message)
		await self.channel_layer.group_send('game', {
			'type': 'reload_page',
			'message': 'reload'
		})

	async def reload_page(self, event):
		# Envoyez le message "reload" à tous les clients
		message = json.dumps(event['message'])
		await self.send(text_data=message)