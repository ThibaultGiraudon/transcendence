from channels.generic.websocket import AsyncWebsocketConsumer
import json

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
		# Send a ping to the WebSocket
		await self.send(text_data=json.dumps({}))