from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync

class StatusConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_group_name = 'status'

		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()


	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

		# Set user offline
		await self.set_user_offline(self.scope["user"].id)


	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		status = text_data_json['status']
		id = text_data_json['id']

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'status_update',
				'status': status,
				'id': id,
			}
		)
	

	async def status_update(self, event):
		status = event['status']
		id = event['id']

		await self.send(text_data=json.dumps({
			'id': id,
			'status': status,
		}))


	@database_sync_to_async
	def set_user_offline(self, user_id):
		User = get_user_model()
		try:
			user = User.objects.get(id=user_id)
			user.status = 'offline'
			user.save()

			# Send a WebSocket message to all other connected clients to inform them that the user is offline
			async_to_sync(self.channel_layer.group_send)(
				self.room_group_name,
				{
					'type': 'status_update',
					'status': 'offline',
					'id': user_id,
				}
			)
		except User.DoesNotExist:
			print(f"User with id {user_id} does not exist")