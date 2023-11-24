from    channels.generic.websocket import AsyncWebsocketConsumer
from    .handlers.handler_init_game import handle_init_game
from    .handlers.handler_paddle_move import handle_paddle_move
from    .handlers.handler_ball_move import handle_ball_move
import  json
import  asyncio

class PongConsumer(AsyncWebsocketConsumer):
    canvasInfo = {
        'width': None,
        'height': None,
    }
    paddlePosition = {
        'left': 100,
        'right': 200,
    }
    ballPosition = {
        'x': 100.0,
        'y': 100.0,
        'speed': 10,
        'direction': 'right',
        'angle': 1.0,
    }
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
        'ball': None,
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
        message = {
            'type': 'init_game',
            'paddlePosition': self.paddlePosition,
            'ballPosition': self.ballPosition,
        }
        await self.send(json.dumps(message))

    async def disconnect(self, close_code):
        if self.tasksAsyncio['ball']:
            self.tasksAsyncio['ball'].cancel()

    async def receive(self, text_data):
        message = json.loads(text_data)
        print(f"Message reçu: {message}")

        if (message['type'] == 'init_game'):
            await handle_init_game(message, self)

        if (message['type'] == 'paddle_move'):
            await handle_paddle_move(message, self)

        if (message['type'] == 'ball_move'):
            self.tasksAsyncio['ball'] = asyncio.create_task(handle_ball_move(self))