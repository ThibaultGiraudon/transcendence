import math
import random

class Ball:
    def __init__(self):
        self.x = 100.0
        self.y = 100.0
        self.radius = 10
        self.color = "0xFDF3E1"
        self.speed = 5
        self.speedBase = 8
        self.angle = 1.0
        self.task = None

    def __powerShot(self, paddle, collisionPosition):
        speedFactor = 1 - abs(collisionPosition - 0.5)
        self.speed = self.speedBase * speedFactor * 1.5
        if (speedFactor > 0.9):
            self.color = paddle.color
            self.radius = 8
        else:
            self.color = "0xFDF3E1"
            self.radius = 10

    def checkPaddleCollision(self, paddle, gameSettings):
        if (paddle.isAlive == False):
            return    

        if (paddle.id == 2 or paddle.id == 3):
            paddleThickness, paddleSize = gameSettings.paddleSize, gameSettings.paddleThickness
            offset, position = paddle.position, paddle.offset
        else:
            paddleThickness, paddleSize = gameSettings.paddleThickness, gameSettings.paddleSize
            offset, position = paddle.offset, paddle.position

        closestX = max(offset, min(self.x, offset + paddleThickness))
        closestY = max(position, min(self.y, position + paddleSize))
        distance = math.sqrt((self.x - closestX)**2 + (self.y - closestY)**2)

        if distance < self.radius:
            if (paddle.id == 2 or paddle.id == 3):
                collisionPosition = (closestX - offset) / paddleThickness
            else:
                collisionPosition = (closestY - position) / paddleSize
            reflectionAngle = (collisionPosition - 0.5) * math.pi
            maxAngle = math.pi / 3

            if (paddle.id == 0):
                self.angle = max(-maxAngle, min(maxAngle, reflectionAngle))
            elif (paddle.id == 1):
                self.angle = math.pi - max(-maxAngle, min(maxAngle, reflectionAngle))
            elif (paddle.id == 2):
                self.angle = math.pi / 2 - max(-maxAngle, min(maxAngle, reflectionAngle))
            elif (paddle.id == 3):
                self.angle = -math.pi / 2 + max(-maxAngle, min(maxAngle, reflectionAngle))

            self.__powerShot(paddle, collisionPosition)

    def checkWallCollision(self, gameSettings):
        maxPosition = gameSettings.squareSize - gameSettings.limit
        for paddle in gameSettings.paddles:
            if (paddle.isAlive == True):
                if (paddle.id == 0 and self.x <= 0):
                    return (0)
                elif (paddle.id == 1 and self.x >= gameSettings.squareSize):
                    return (1)
                elif (paddle.id == 2 and self.y <= 0):
                    return (2)
                elif (paddle.id == 3 and self.y >= gameSettings.squareSize):
                    return (3)
            else:
                if (paddle.id == 0 and self.x <= gameSettings.limit):
                    self.angle = math.pi - self.angle
                elif (paddle.id == 1 and self.x >= maxPosition):
                    self.angle = math.pi - self.angle
                elif (paddle.id == 2 and self.y <= gameSettings.limit):
                    self.angle = -self.angle
                elif (paddle.id == 3 and self.y >= maxPosition):
                    self.angle = -self.angle
        return (-1)

    def move(self):
        deltaX = self.speed * math.cos(self.angle) 
        deltaY = self.speed * math.sin(self.angle)
        self.x += deltaX
        self.y += deltaY

    def resetBall(self, gameSettings):
        self.x = gameSettings.squareSize / 2
        self.y = gameSettings.squareSize / 2
        self.radius = 10
        self.color = "0xFDF3E1"
        self.speed = 5

        randomAngle = []
        for paddle in gameSettings.paddles:
            if paddle.isAlive and paddle.id == 0:
                randomAngle.append(math.pi)
            elif paddle.isAlive and paddle.id == 1:
                randomAngle.append(0)
            elif paddle.isAlive and paddle.id == 2:
                randomAngle.append(-math.pi / 2)
            elif paddle.isAlive and paddle.id == 3:
                randomAngle.append(math.pi / 2)
                
        self.angle = random.choice(randomAngle)