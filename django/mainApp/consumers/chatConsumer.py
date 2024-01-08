import json, logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
	@database_sync_to_async
	def create_notification(self, user, message):
		from mainApp.models import Notification
		notification = Notification(user=user, message=message)
		notification.save()


	@database_sync_to_async
	def change_status_to_online(self):
		User = get_user_model()
		user = User.objects.get(id=self.scope['user'].id)
		user.status = 'online'
		user.save()
		

	@database_sync_to_async
	def get_users(self, room_id):
		users = []

		from mainApp.models import Channel
		try:
			channel = Channel.objects.get(room_id=room_id)
			for user in channel.users.all():
				if user.id != self.scope['user'].id:
					users.append(user)
			
			return users
		except Channel.DoesNotExist:
			return None
		

	async def connect(self):
		self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
		self.room_group_name = f"chat_{self.room_id}"

		# Join room group
		await self.channel_layer.group_add(self.room_group_name, self.channel_name)
		await self.accept()

		#await self.send_previous_messages()
	

	@database_sync_to_async
	def get_previous_messages(self):
		from mainApp.models import Channel
		
		# Get the channel
		try:
			channel = Channel.objects.get(room_id=self.room_id)
		except Channel.DoesNotExist:
			return []
		
		return channel.messages


	async def send_previous_messages(self):
		# Get messages and sort them
		previous_messages = await self.get_previous_messages()
		if previous_messages is None or len(previous_messages) == 0:
			return
		previous_messages.sort(key=lambda msg: msg['timestamp'])

		# Send the previous messages
		for message in previous_messages:
			await self.send(text_data=json.dumps(message))


	async def disconnect(self, close_code):
		await self.change_status_to_online()
		await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

		self.room_id = None
		self.room_group_name = None


	async def receive(self, text_data):
		# Receive message from WebSocket
		text_data_json = json.loads(text_data)
		message = text_data_json.get("message")
		sender = text_data_json.get("sender")
		username = text_data_json.get("username")
		timestamp = datetime.now().isoformat()

		# Get the user
		user = self.scope['user']

		# Save the message
		await self.save_message(sender, username, message, timestamp)

		# Get the channel
		channel = await self.get_channel()

		if channel is None:
			return

		# Get the users
		usersToSend = await self.get_users(self.room_id)

		# Send a notification to the users
		if usersToSend is not None:
			for userToSend in usersToSend:
				if userToSend.status != f"chat:{self.room_id}":
					if self.scope['user'].id not in userToSend.blockedUsers:
						await self.create_notification(userToSend, f"You have a new message from {channel.name}")
		
		# Send message to room group
		await self.channel_layer.group_send(
			self.room_group_name, {"type": "chat_message", "message": message, "sender": sender, "username": username, "timestamp": timestamp}
		)
	

	@database_sync_to_async
	def get_channel(self):
		from mainApp.models import Channel
		try:
			return Channel.objects.get(room_id=self.room_id)
		except Channel.DoesNotExist:
			return None


	@database_sync_to_async
	def save_message(self, sender, username, message, timestamp):
		from mainApp.models import Channel
		
		# Get the channel
		try:
			channel = Channel.objects.get(room_id=self.room_id)
		except Channel.DoesNotExist:
			return
		
		if channel.messages is None:
			channel.messages = []

		# Save the message
		channel.messages.append({ "sender": sender, "username": username, "message": message, "timestamp": timestamp })
		channel.save()


	async def chat_message(self, event):
		# Receive message from room group
		message = event.get("message")
		sender = event.get("sender")
		username = event.get("username")

		# Send message to WebSocket
		await self.send(text_data=json.dumps({"message": message, "sender": sender, "username": username}))