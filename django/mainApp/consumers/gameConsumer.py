from    channels.generic.websocket import AsyncWebsocketConsumer
from 	channels.db import database_sync_to_async
from    ..pongFunctions.handlerInitGame import handle_init_game
from    ..pongFunctions.handlerPaddleMove import handle_paddle_move
from    ..pongFunctions.gameSettingsClass import GameSettings
import  json

class GameConsumer(AsyncWebsocketConsumer):
	gameSettings = GameSettings(800)

	@database_sync_to_async
	def handleInitGame(self, gameID, gameMode, playerID):
		# TODO ici si tout les joeurs sont prêt on lance le jeu
		from mainApp.models import Game, Player
		game = Game.objects.get(id=gameID)
		if playerID not in game.playerList:
			print("player not in game")
			return (False)

		player = Player.objects.get(id=playerID)
		player.isReady = True
		player.save()

		for playerID in game.playerList:
			player = Player.objects.get(id=playerID)
			if (player.isReady == False):
				return (False)

		# TODO ici on lance le jeu
		return (True)

	async def connect(self):
		await self.channel_layer.group_add('game', self.channel_name)
		await self.accept()

	async def disconnect(self, close_code):
		# if (self.gameSettings.ball.task):
			# self.gameSettings.ball.task.cancel()
		await self.channel_layer.group_discard('game', self.channel_name)

	async def receive(self, text_data):
		gameID = self.scope['url_route']['kwargs']['game_id']
		message = json.loads(text_data)
		print(message)

		if (message['type'] == 'init_ranked_solo_game'):
			await self.handleInitGame(gameID, message['type'], message['playerID'])

		await self.channel_layer.group_send('game', {
			'type': 'reload_page',
			'message': 'reload'
		})

	async def init_ranked_solo_game(self, event):
		print('init_ranked_solo_game')
		message = json.dumps(event['message'])
		print(message)

	async def reload_page(self, event):
		# Envoyez le message "reload" à tous les clients
		message = json.dumps(event['message'])
		await self.send(text_data=message)