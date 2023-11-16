from channels.generic.websocket import AsyncWebsocketConsumer
import json

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print('connected')
        await self.send(text_data=json.dumps({
            'type': 'echo',
            'message': 'Htllo',
        }))

    async def disconnect(self, close_code):
        print('disconnected')

    async def receive(self, text_data):
        message = json.loads(text_data)
        await self.send(text_data=json.dumps({
            'type': 'echo',
            'message': message['message'],
        }))