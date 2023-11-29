from    channels.generic.websocket import AsyncWebsocketConsumer
from    .handlers.handler_init_game import handle_init_game
from    .handlers.handler_paddle_move import handle_paddle_move
from    .gameObjects import *
import  json

class PongConsumer(AsyncWebsocketConsumer):
    gameSettings = GameSettings(2)

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        if (self.ball.task):
            self.ball.task.cancel()

    async def receive(self, text_data):
        message = json.loads(text_data)
        # print(f"Message reçu: {message}")

        if (message['type'] == 'init_game'):
            await handle_init_game(message, self)

        if (message['type'] == 'paddle_move'):
            await handle_paddle_move(message, self)