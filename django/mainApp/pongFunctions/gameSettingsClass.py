from .paddleClass import Paddle
from .ballClass import Ball

class GameSettings:
    def __init__(self, nbPaddles, size):
        self.nbPaddles = nbPaddles
        self.squareSize = size;
        self.paddles = []
        self.ball = Ball()
        self.offset = 20
        self.paddleThickness = 20
        self.paddleSize = 100
        self.limit = self.offset + self.paddleThickness

        for id in range(4):
            self.paddles.append(Paddle(id))
            self.paddles[id].position = self.squareSize / 2 - self.paddleSize / 2
            if (id % 2 == 0):
                self.paddles[id].offset = self.offset
            else:
                self.paddles[id].offset = self.squareSize - self.limit

        for id in range(self.nbPaddles):
            self.paddles[id].isAlive = True