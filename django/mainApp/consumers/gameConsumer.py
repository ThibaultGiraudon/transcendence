from    channels.generic.websocket import AsyncWebsocketConsumer
from 	channels.db import database_sync_to_async
import  json

from    .gameConsumerUtils.classes.gameSettings import GameSettings
from	.gameConsumerUtils.sendInitPaddlePosition import sendInitPadlePosition
from 	.gameConsumerUtils.handlePaddleMove import handlePaddleMove
from	.gameConsumerUtils.handleBallMove import handleBallMove

gameSettings_instances = {}

class GameConsumer(AsyncWebsocketConsumer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.gameSettings_instances = gameSettings_instances

	# gameSettings = GameSettings(800)
	# gameSettings.setNbPaddles(2)
	# print('gameSettings pos', gameSettings.paddles[0].position)
	# def __init__(self, *args, **kwargs):
		# super().__init__(*args, **kwargs)
		# self.gameSettings = GameSettings(800)
	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	if not hasattr(self, 'gameSettings') or self.gameSettings is None:
	# 		self.gameSettings = self.gameSettings_instances.get(self.scope['url_route']['kwargs']['game_id'])
	# 		# self.gameSettings = GameSettings(800)
	# 		self.gameSettings.setNbPaddles(2)

	async def launchRankedSoloGame(self, gameID, gameMode):
		if gameID not in self.gameSettings_instances:
			self.gameSettings_instances[gameID] = GameSettings(800)
			self.gameSettings_instances[gameID].setNbPaddles(2)

		gameSettings = self.gameSettings_instances[gameID]
		await sendInitPadlePosition(self, gameSettings)
			# self.gameSettings.setNbPaddles(2)
			# await sendInitPadlePosition(self)
		# await handleBallMove(self, gameMode)

	# TODO peut-etre inutile si on fait tout dans la premiere fonction
	# def launchDeathGame(self):
	# 	print('-----------------------------///launchDeathGame')

	# def launchTournamentGame(self):
	# 	print('-----------------------------///launchTournamentGame')

	@database_sync_to_async
	def __getGame(self, gameID):
		from mainApp.models import Game
		return Game.objects.get(id=gameID)

	@database_sync_to_async
	def __getPlayer(self, playerID):
		from mainApp.models import Player
		return Player.objects.get(id=playerID)

	@database_sync_to_async
	def __savePlayer(self, player):
		player.save()

	async def handleInitGame(self, gameID, gameMode, playerID):
		game = await self.__getGame(gameID)
		if playerID not in game.playerList:
			return (False)

		player = await self.__getPlayer(playerID)
		player.isReady = True
		await self.__savePlayer(player)

		for playerID in game.playerList:
			player = await self.__getPlayer(playerID)
			if not player.isReady:
				return (False)

		if (gameMode == 'init_ranked_solo_game'):
			await self.launchRankedSoloGame(gameID, gameMode)
		# elif (gameMode == 'init_death_game'):
		# 	self.launchDeathGame()
		# elif (gameMode == 'init_tournament_game'):
		# 	self.launchTournamentGame()
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
		# # TODO add other local game modes
		# # else if (message['type'] == 'init_solooo'):
		# 	# await handle_paddle_move(self, message['paddleID'], message['direction'])

		if (message['type'] == 'paddle_move'):
			gameSettings = self.gameSettings_instances[gameID]
			await handlePaddleMove(self, message, gameSettings)

		# print('receive from consumer ----')
		# # TODO use this to send reload to waiting players
		# await self.channel_layer.group_send('game', {
		# 	'type': 'reload_page',
		# 	'message': 'reload'
		# })

	# TODO use this to send reload to waiting players
	async def reload_page(self, event):
		message = json.dumps(event)
		await self.send(text_data=message)

	async def init_paddle_position(self, event):
		message = json.dumps(event)
		await self.send(text_data=message)

	async def update_paddle_position(self, event):
		message = json.dumps(event)
		await self.send(text_data=message)