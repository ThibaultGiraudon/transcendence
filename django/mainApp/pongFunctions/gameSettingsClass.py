from .paddleClass import Paddle
from .ballClass import Ball

class GameSettings:
    def __init__(self, size):
        self.nbPaddles = None
        self.squareSize = size
        self.paddles = []
        self.ball = None
        self.paddleSize = 100

        # self.nbPaddles = None
        # self.squareSize = size
        # self.paddles = []
        # self.ball = None
        # self.offset = 20
        # self.paddleThickness = 20
        # self.paddleSize = 100
        # self.limit = self.offset + self.paddleThickness
        # self.isAIGame = False

    # def setNbPaddles(self, nbPaddles):
        # self.nbPaddles = nbPaddles
        # for id in range(4):
        #     self.paddles.append(Paddle(id))
        #     self.paddles[id].position = self.squareSize / 2 - self.paddleSize / 2
        #     if (id % 2 == 0):
        #         self.paddles[id].offset = self.offset
        #     else:
        #         self.paddles[id].offset = self.squareSize - self.limit

    #     for id in range(self.nbPaddles):
    #         self.paddles[id].isAlive = True

    #     self.ball = Ball(self)
        
    # def setIsAIGame(self, isAIGame):
    #     self.isAIGame = isAIGame

# class GameSettings:
    # def __init__(self, size):
        # self.nbPaddles = None
        # self.squareSize = size
        # self.paddles = []
        # self.ball = None
        # self.offset = 20
        # self.paddleThickness = 20
        # self.paddleSize = 100
        # self.limit = self.offset + self.paddleThickness
        # self.isAIGame = False
# 
    # def setNbPaddles(self, nbPaddles):
        # self.nbPaddles = nbPaddles
        # for id in range(4):
            # self.paddles.append(Paddle(id))
            # self.paddles[id].position = self.squareSize / 2 - self.paddleSize / 2
            # if (id % 2 == 0):
                # self.paddles[id].offset = self.offset
            # else:
                # self.paddles[id].offset = self.squareSize - self.limit
# 
        # for id in range(self.nbPaddles):
            # self.paddles[id].isAlive = True
# 
        # self.ball = Ball(self)
        # 
    # def setIsAIGame(self, isAIGame):
        # self.isAIGame = isAIGame