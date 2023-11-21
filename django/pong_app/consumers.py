from    channels.generic.websocket import AsyncWebsocketConsumer
from    .handlers.handler_paddle_move import handle_paddle_move
from    .handlers.handler_init_game import handle_init_game
import  json

class PongConsumer(AsyncWebsocketConsumer):
    paddlePosition = 0
    # keyState = {
        # 'ArrowUp': False,
        # 'ArrowDown': False,
    # }
    keyState = {
        'left': {
            'up': False,
            'down': False,
        },
        'right': {
            'up': False,
            'down': False,
        },
    }
    tasksAsyncio = {
        'left': {
            'up': None,
            'down': None,
        },
        'right': {
            'up': None,
            'down': None,
        },
    }

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