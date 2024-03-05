from .paddle import Paddle
from .ball import Ball

class GameSettings:
    _instances = {}

    def __new__(cls, gameID, *args, **kwargs):
        if gameID not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[gameID] = instance
        return cls._instances[gameID]

    def __init__(self, gameID, gameMode):
        self.gameID = gameID
        self.gameMode = gameMode
        print('GameSettings init')

        if (gameMode in ['init_ranked_solo_game', 'init_tournament_game', 'init_local_game']):
            self.nbPaddles = 2
            self.isAIGame = False
        elif (gameMode in ['init_death_game']):
            self.nbPaddles = 4
            self.isAIGame = False
        elif (gameMode == 'init_ai_game'):
            self.nbPaddles = 2
            self.isAIGame = True
        elif (gameMode == 'init_wall_game'):
            self.nbPaddles = 1
            self.isAIGame = False

        self.squareSize = 800
        self.paddles = []
        self.playerIDList = []
        self.paddleSize = 100
        self.paddleThickness = 20
        self.offset = 20
        self.limit = self.offset + self.paddleThickness
        self.isLocalGame = False

        for id in range(4):
            self.paddles.append(Paddle(id))
            self.paddles[id].isAlive = False

        for id in range(self.nbPaddles):
            self.paddles[id].position = self.squareSize / 2 - self.paddleSize / 2
            self.paddles[id].isAlive = True

            if (id % 2 == 0):
                self.paddles[id].offset = self.offset
            else:
                self.paddles[id].offset = self.squareSize - self.limit

        self.ball = Ball(self)