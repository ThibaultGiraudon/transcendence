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
    def __init__(self, nbPaddles):
        print('GameSettings init')
        self.nbPaddles = nbPaddles
        self.squareSize = 800
        self.paddles = []
        self.paddleSize = 100

        for id in range(nbPaddles):
            self.paddles.append(Paddle(id))
            self.paddles[id].position = self.squareSize / 2 - self.paddleSize / 2
            self.paddles[id].isAlive = True

        self.ball = Ball(self)