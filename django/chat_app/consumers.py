import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
		self.room_group_name = f"chat_{self.room_name}"

		# Join room group
		await self.channel_layer.group_add(self.room_group_name, self.channel_name)
		await self.accept()

		# Send previous messages
		

	async def disconnect(self, close_code):
		# Leave room group
		await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

	# Receive message from WebSocket
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json.get("message")
		sender = text_data_json.get("sender")

		# Save message
		

		# Send message to room group
		await self.channel_layer.group_send(
			self.room_group_name, {"type": "chat_message", "message": message, "sender": sender}
		)

	# Receive message from room group
	async def chat_message(self, event):
		message = event.get("message")
		sender = event.get("sender")

		# Send message to WebSocket
		await self.send(text_data=json.dumps({"message": message, "sender": sender}))