from    channels.generic.websocket import AsyncWebsocketConsumer
from    ..pongFunctions.handlerInitGame import handle_init_game
from    ..pongFunctions.handlerPaddleMove import handle_paddle_move
from    ..pongFunctions.gameSettingsClass import GameSettings
import  json

class PongConsumer(AsyncWebsocketConsumer):
	gameSettings = GameSettings(800)

	async def connect(self):
		await self.accept()

	async def disconnect(self, close_code):
		if (self.gameSettings.ball.task):
			self.gameSettings.ball.task.cancel()

	async def receive(self, text_data):
		message = json.loads(text_data)

		if (message['type'] == 'init_local_game'):
			self.gameSettings.setNbPaddles(2)
			await handle_init_game(self, message['type'])

		if (message['type'] == 'init_ai_game'):
			self.gameSettings.setNbPaddles(2)
			self.gameSettings.setIsAIGame(True)
			await handle_init_game(self, message['type'])

		if (message['type'] == 'paddle_move'):
			await handle_paddle_move(message, self)


class TestConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		game_id = self.scope['url_route']['kwargs']['game_id']
		self.game_group_name = f'game_{game_id}'

		await self.channel_layer.group_add(
			self.game_group_name,
			self.channel_name
		)

		await self.accept()

	async def disconnect(self, close_code):
		# Déconnectez-vous du groupe WebSocket correspondant au jeu
		await self.channel_layer.group_discard(
			self.game_group_name,
			self.channel_name
		)

	async def receive(self, text_data):
		# Traitez les messages reçus du client WebSocket
		print(text_data)

	async def notify_players(self):
		# Envoyez un message aux autres joueurs pour leur demander de recharger la page
		await self.channel_layer.group_send(
			self.game_group_name,
			{
				'type': 'reload_page',
			}
		)

	async def reload_page(self, event):
		# Répondez au message de rechargement de page
		await self.send(text_data='reload')
