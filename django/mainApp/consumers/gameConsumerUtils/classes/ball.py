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

    def __getRandomAngle(self, gameSettings):
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
        return (randomAngle)

    def __getReflectionAngle(self, paddle, maxAngle, reflectionAngle):
        if (paddle.id == 0):
            self.angle = max(-maxAngle, min(maxAngle, reflectionAngle))
        elif (paddle.id == 1):
            self.angle = math.pi - max(-maxAngle, min(maxAngle, reflectionAngle))
        elif (paddle.id == 2):
            self.angle = math.pi / 2 - max(-maxAngle, min(maxAngle, reflectionAngle))
        elif (paddle.id == 3):
            self.angle = -math.pi / 2 + max(-maxAngle, min(maxAngle, reflectionAngle))

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
        
        print('distance', distance, 'paddle', paddle.id)

        # if distance < self.radius:
        #     if (paddle.id == 2 or paddle.id == 3):
        #         collisionPosition = (closestX - offset) / paddleThickness
        #     else:
        #         collisionPosition = (closestY - position) / paddleSize
        #     reflectionAngle = (collisionPosition - 0.5) * math.pi
        #     maxAngle = math.pi / 3

        #     self.__getReflectionAngle(paddle, maxAngle, reflectionAngle)
            # TODO add powershot
            # self.__powerShot(paddle, collisionPosition)

    def move(self):
        deltaX = self.speed * math.cos(self.angle) 
        deltaY = self.speed * math.sin(self.angle)
        self.x += deltaX
        self.y += deltaY