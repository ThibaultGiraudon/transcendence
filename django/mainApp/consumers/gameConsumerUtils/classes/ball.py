import math
import random

class Ball:
    def __init__(self, gameSettings):
        self.x = gameSettings.squareSize / 2
        self.y = gameSettings.squareSize / 2
        self.radius = 10
        # self.color = "0xFDF3E1"
        self.speed = 5
        self.speedBase = 10
        self.task = None

        randomAngle = self.__getRandomAngle(gameSettings)
        self.angle = random.choice(randomAngle)

    def move(self):
        deltaX = self.speed * math.cos(self.angle) 
        deltaY = self.speed * math.sin(self.angle)
        self.x += deltaX
        self.y += deltaY