from    channels.generic.websocket import AsyncWebsocketConsumer
from 	channels.db import database_sync_to_async
# from    ..pongFunctions.handlerInitGame import handle_init_game
# from    ..pongFunctions.handlerPaddleMove import handle_paddle_move
from    ..pongFunctions.gameSettingsClass import GameSettings
import  json
from	asgiref.sync import async_to_sync

from	.gameConsumerUtils.sendInitPaddlePosition import sendInitPadlePosition
from 	.gameConsumerUtils.handlePaddleMove import handlePaddleMove

class GameConsumer(AsyncWebsocketConsumer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not hasattr(self, 'gameSettings') or self.gameSettings is None:
			self.gameSettings = GameSettings(800)

	def launchRankedSoloGame(self, gameID, gameMode):
		self.gameSettings = GameSettings(800)
		self.gameSettings.setNbPaddles(2)
		sendInitPadlePosition(self)

	# TODO peut-etre inutile si on fait tout dans la premiere fonction
	# def launchDeathGame(self):
	# 	print('-----------------------------///launchDeathGame')

	# def launchTournamentGame(self):
	# 	print('-----------------------------///launchTournamentGame')

	@database_sync_to_async
	def handleInitGame(self, gameID, gameMode, playerID):
		from mainApp.models import Game, Player
		game = Game.objects.get(id=gameID)
		if playerID not in game.playerList:
			return (False)

		player = Player.objects.get(id=playerID)
		player.isReady = True
		player.save()

		for playerID in game.playerList:
			player = Player.objects.get(id=playerID)
			if (player.isReady == False):
				return (False)

		if (gameMode == 'init_ranked_solo_game'):
			self.launchRankedSoloGame(gameID, gameMode)
		elif (gameMode == 'init_death_game'):
			self.launchDeathGame()
		elif (gameMode == 'init_tournament_game'):
			self.launchTournamentGame()
		return (True)

	async def connect(self):
		await self.channel_layer.group_add('game', self.channel_name)
		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard('game', self.channel_name)

	async def receive(self, text_data):
		gameID = self.scope['url_route']['kwargs']['game_id']
		message = json.loads(text_data)
		print(message)

		if (message['type'] == 'init_ranked_solo_game' or \
	  		message['type'] == 'init_death_game' or \
	  		message['type'] == 'init_tournament_game'):
			await self.handleInitGame(gameID, message['type'], message['playerID'])
		# TODO add other local game modes
		# else if (message['type'] == 'init_solooo'):
			# await handle_paddle_move(self, message['paddleID'], message['direction'])

		if (message['type'] == 'paddle_move'):
			await handlePaddleMove(self, message)

		# TODO use this to send reload to waiting players
		# await self.channel_layer.group_send('game', {
		# 	'type': 'reload_page',
		# 	'message': 'reload'
		# })

	# TODO use this to send reload to waiting players
	async def reload_page(self, event):
		message = json.dumps(event['message'])
		await self.send(text_data=message)

	async def init_paddle_position(self, event):
		message = json.dumps(event)
		await self.send(text_data=message)

	async def update_paddle_position(self, event):
		message = json.dumps(event)
		await self.send(text_data=message)