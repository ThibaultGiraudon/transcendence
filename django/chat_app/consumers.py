import json, logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
	
	@database_sync_to_async
	def create_notification(self, user, message):
		from users_app.models import Notification
		notification = Notification(user=user, message=message)
		notification.save()

	
	@database_sync_to_async
	def change_status_to_online(self):
		self.scope['user'].status = 'online'
		self.scope['user'].save()
	

	@database_sync_to_async
	def get_user_to(self, room_name):
		User = get_user_model()
		users = User.objects.all()
		for user in users:
			if room_name in user.channels.values() and user.username != self.scope["user"].username:
				return user
		return None
		
		
	async def connect(self):
		self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
		self.room_group_name = f"chat_{self.room_name}"

		# Join room group
		await self.channel_layer.group_add(self.room_group_name, self.channel_name)
		await self.accept()

		# Send previous messages
		await self.send_previous_messages()

	
	# Get previous messages
	@database_sync_to_async
	def get_previous_messages(self):
		User = get_user_model()
		messages = []
		for user in User.objects.all():
			if self.room_name in user.messages:
				messages.extend(user.messages[self.room_name])
		return messages


	async def send_previous_messages(self):
		previous_messages = await self.get_previous_messages()
		previous_messages.sort(key=lambda msg: msg['timestamp'])
		for message in previous_messages:
			await self.send(text_data=json.dumps(message))
  

	async def disconnect(self, close_code):
		# Set status to online
		await self.change_status_to_online()

		# Leave room group
		await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


	# Receive message from WebSocket
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json.get("message")
		sender = text_data_json.get("sender")
		timestamp = datetime.now().isoformat()

		# Save message
		await self.save_message(sender, message, timestamp)

		# Get the user to send
		userTo = await self.get_user_to(self.room_name)
		
		# Send a notification
		if userTo is not None and userTo.status != f"chat:{self.scope['user'].username}":
			await self.create_notification(userTo, f"You have a new message from {sender}.")

		# Send message to room group
		await self.channel_layer.group_send(
			self.room_group_name, {"type": "chat_message", "message": message, "sender": sender, "timestamp": timestamp}
		)


	# Save messages
	@database_sync_to_async
	def save_message(self, sender, message, timestamp):
		User = get_user_model()
		user = User.objects.get(username=sender)
		if self.room_name not in user.messages:
			user.messages[self.room_name] = []
		user.messages[self.room_name].append({'sender': sender, 'message': message, 'timestamp': timestamp})
		user.save()


	# Receive message from room group
	async def chat_message(self, event):
		message = event.get("message")
		sender = event.get("sender")

		# Send message to WebSocket
		await self.send(text_data=json.dumps({"message": message, "sender": sender}))