from .paddle import Paddle
from .ball import Ball

def singleton(class_):
    instances = {}

    def wrapper(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return wrapper

@singleton
class GameSettings:
    def __init__(self, size):
        print('GameSettings init')
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
        self.ball = Ball(self)