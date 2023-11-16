from channels.generic.websocket import AsyncWebsocketConsumer
import json

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        message = json.loads(text_data)
        await self.send(text_data=json.dumps({
            'type': 'echo',
            'message': message['message'],
        }))