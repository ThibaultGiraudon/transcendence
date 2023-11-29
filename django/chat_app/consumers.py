import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

messages = {}

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        logging.info("----------------\nCONNECT")
        logging.info("coucou1")
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        logging.info("----------------\nCONNECT")
        logging.info("coucou2")
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)


        await self.accept()

        if self.room_name in messages:
            for message in messages[self.room_name]:
                await self.send(text_data=json.dumps({"message": message[1], "sender": message[0]}))
            
    async def disconnect(self, close_code):
        # Leave room group
        logging.info("----------------\nDISCONNECT")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        logging.info("----------------\nRECEIVE")
        logging.info(text_data_json)
        message = text_data_json.get("message")
        sender = text_data_json.get("sender")

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message, "sender": sender}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event.get("message")
        sender = event.get("sender")
        logging.info("----------------\nCHAT_MESSAGE")
        logging.info(self.room_name)

        if self.room_name not in messages:
            messages[self.room_name] = []
        messages[self.room_name].append([sender, message])

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "sender": sender}))