from    channels.generic.websocket import AsyncWebsocketConsumer
import  json

from    .gameConsumerUtils.classes.gameSettings import GameSettings
from 	.gameConsumerUtils.handlePaddleMove import handlePaddleMove
from	.gameConsumerUtils.handleInitGame import handleInitGame

gameSettingsInstances = {}

class GameConsumer(AsyncWebsocketConsumer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.gameSettingsInstances = gameSettingsInstances

	# TODO peut-etre inutile si on fait tout dans la premiere fonction
	# def launchDeathGame(self):
	# 	print('-----------------------------///launchDeathGame')

	# def launchTournamentGame(self):
	# 	print('-----------------------------///launchTournamentGame')

	async def connect(self):
		await self.channel_layer.group_add('game', self.channel_name)
		await self.accept()

	async def disconnect(self, close_code):
		# TODO inutile car si on quitte la page ca delete la ball (a reverifier quand meme)
		# gameID = self.scope['url_route']['kwargs']['game_id']
		# if (gameID in self.gameSettingsInstances):
		# 	GameSettings = self.gameSettingsInstances[gameID]
		# 	if (GameSettings.ball.task):
		#		GameSettings.ball.task.cancel()
		await self.channel_layer.group_discard('game', self.channel_name)

	async def receive(self, text_data):
		gameID = self.scope['url_route']['kwargs']['game_id']
		message = json.loads(text_data)

		if (message['type'] == 'init_ranked_solo_game' or \
			message['type'] == 'init_death_game' or \
			message['type'] == 'init_tournament_game'):
				await handleInitGame(self, gameID, message['type'], message['playerID'])
		# # TODO add other local game modes
		# # else if (message['type'] == 'init_solooo'):
		# 	# await handle_paddle_move(self, message['paddleID'], message['direction'])

		if (message['type'] == 'paddle_move'):
			gameSettings = self.gameSettingsInstances[gameID]
			await handlePaddleMove(self, message, gameSettings)

		# print('receive from consumer ----')
		# # TODO use this to send reload to waiting players
		# await self.channel_layer.group_send('game', {
		# 	'type': 'reload_page',
		# })

	# Called by the server when a message is received from the group
	async def reload_page(self, event):
		message = json.dumps(event)
		await self.send(text_data=message)

	async def init_paddle_position(self, event):
		message = json.dumps(event)
		await self.send(text_data=message)

	async def init_score(self, event):
		message = json.dumps(event)
		await self.send(text_data=message)

	async def update_paddle_position(self, event):
		message = json.dumps(event)
		await self.send(text_data=message)

	async def update_ball_position(self, event):
		message = json.dumps(event)
		await self.send(text_data=message)