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

	async def connect(self):
		self.game_id = self.scope['url_route']['kwargs']['game_id']
		self.game_group_name = f'game_{self.game_id}'

		await self.channel_layer.group_add(
			self.game_group_name,
			self.channel_name
		)
		await self.accept()

	async def disconnect(self, close_code):
		# TODO inutile car si on quitte la page ca delete la ball (a reverifier quand meme)
		# gameID = self.scope['url_route']['kwargs']['game_id']
		# if (gameID in self.gameSettingsInstances):
		# 	GameSettings = self.gameSettingsInstances[gameID]
		# 	if (GameSettings.ball.task):
		#		GameSettings.ball.task.cancel()
		await self.channel_layer.group_discard(
			self.game_group_name,
			self.channel_name
		)

	async def receive(self, text_data):
		gameID = self.scope['url_route']['kwargs']['game_id']
		message = json.loads(text_data)

		if (message['type'] == 'init_ranked_solo_game' or \
			message['type'] == 'init_death_game' or \
			message['type'] == 'init_tournament_game' or \
			message['type'] == 'init_local_game' or \
			message['type'] == 'init_ai_game' or \
			message['type'] == 'init_wall_game'):
			await handleInitGame(self, gameID, message['type'], message['playerID'])

		if (message['type'] == 'paddle_move'):
			gameSettings = self.gameSettingsInstances[gameID]
			await handlePaddleMove(self, message, gameSettings, message['playerID'])

	# Called by the server when a message is received from the group
	async def reload_page(self, event):
		message = json.dumps(event)
		await self.send(text_data=message)

	async def init_paddle_position(self, event):
		message = json.dumps(event)
		await self.send(text_data=message)

	async def update_score(self, event):
		message = json.dumps(event)
		await self.send(text_data=message)

	async def update_paddle_position(self, event):
		message = json.dumps(event)
		await self.send(text_data=message)

	async def update_ball_position(self, event):
		message = json.dumps(event)
		await self.send(text_data=message)