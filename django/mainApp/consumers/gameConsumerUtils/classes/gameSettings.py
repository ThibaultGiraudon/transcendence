from .paddle import Paddle
from .ball import Ball

# def singleton(class_):
#     instances = {}

#     def wrapper(*args, **kwargs):
#         if class_ not in instances:
#             instances[class_] = class_(*args, **kwargs)
#         return instances[class_]

#     return wrapper

# @singleton
class GameSettings:
    _instances = {}

    def __new__(cls, gameID, *args, **kwargs):
        if gameID not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[gameID] = instance
        return cls._instances[gameID]

    def __init__(self, gameID, nbPaddles, isAIGame):
        self.gameID = gameID
        print('GameSettings init')
        self.nbPaddles = nbPaddles
        self.isAIGame = isAIGame
        self.squareSize = 800
        self.paddles = []
        self.playerIDList = []
        self.paddleSize = 100
        self.paddleThickness = 20
        self.offset = 20
        self.limit = self.offset + self.paddleThickness

        for id in range(4):
            self.paddles.append(Paddle(id))
            self.paddles[id].isAlive = False

        for id in range(nbPaddles):
            self.paddles[id].position = self.squareSize / 2 - self.paddleSize / 2
            self.paddles[id].isAlive = True

            if (id % 2 == 0):
                self.paddles[id].offset = self.offset
            else:
                self.paddles[id].offset = self.squareSize - self.limit

        self.ball = Ball(self)