from    channels.generic.websocket import AsyncWebsocketConsumer
from    .handlers.handler_paddle_move import handle_paddle_move
from    .handlers.handler_init_game import handle_init_game
import  json
import  asyncio

class PongConsumer(AsyncWebsocketConsumer):
    paddle_position = 0
    moving = False;

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        message = json.loads(text_data)
        print(f"Message reçu: {message}")

        if (message['type'] == 'init_game'):
            await handle_init_game(message, self)

        if (message['type'] == 'paddle_move'):
            await handle_paddle_move(message, self)