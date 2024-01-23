from    channels.generic.websocket import AsyncWebsocketConsumer
# from	..models import Game
from    ..pongFunctions.handlerInitGame import handle_init_game
from    ..pongFunctions.handlerPaddleMove import handle_paddle_move
from    ..pongFunctions.gameSettingsClass import GameSettings
import  json

async def handleInitGame(consumer, gameID, gameMode, playerID):
	# try:
		# game = Game.objects.get(id=gameID)
	# except Game.DoesNotExist:
		# return (False)
	# if playerID not in game.playerList:
	# 	return (False)
	# consumer.playerList.append(playerID)

	# for player in consumer.playerList:
	# 	print(player)
	
	return (True)

class GameConsumer(AsyncWebsocketConsumer):
	gameSettings = GameSettings(800)
	playerList = []

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
			await handleInitGame(self, gameID, message['type'], message['playerID'])

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