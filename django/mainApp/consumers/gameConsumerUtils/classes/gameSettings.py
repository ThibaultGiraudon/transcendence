from .paddle import Paddle
from .ball import Ball

class GameSettings:
    def __init__(self, size):
        self.nbPaddles = None
        self.squareSize = size
        self.paddles = []
        self.ball = None
        self.paddleSize = 100

    def setNbPaddles(self, nbPaddles):
        self.nbPaddles = nbPaddles
        for id in range(nbPaddles):
            self.paddles.append(Paddle(id))
            self.paddles[id].position = self.squareSize / 2 - self.paddleSize / 2
            self.paddles[id].isAlive = True