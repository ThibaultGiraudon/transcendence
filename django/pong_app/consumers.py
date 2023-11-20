from    channels.generic.websocket import AsyncWebsocketConsumer
from    .handlers.handler_paddle_move import *
import  json
import  asyncio

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        position = 100;
        await self.send(json.dumps({'type': 'update_paddle_position', 'position': position}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        message = json.loads(text_data)
        print(f"Message reçu: {message}")

        if (message['type'] == 'paddle_move'):
            await handle_paddle_move(message, self)
            # direction = message['direction']
            # if (direction == 'ArrowUp'):
                # position = 0
                # await self.send(json.dumps({'type': 'update_paddle_position', 'position': position}))
            # elif (direction == 'ArrowDown'):
                # position = 400
                # await self.send(json.dumps({'type': 'update_paddle_position', 'position': position}))