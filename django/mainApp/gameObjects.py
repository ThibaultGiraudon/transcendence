import math
import random

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

        for id in range(self.nbPaddles):
            self.paddles.append(Paddle(id))
            self.paddles[id].position = self.squareSize / 2 - self.paddleSize / 2
        
        for id in range(self.nbPaddles):
            if (id % 2 == 0):
                self.paddles[id].offset = self.offset
            else:
                self.paddles[id].offset = self.squareSize - self.limit

class Paddle:
    def __init__(self, id):
        self.id = id
        self.offset = 0
        self.position = 0
        self.paddleThickness = 20
        self.paddleSize = 100
        self.speed = 10
        self.score = 0
        self.keyState = {
            'up': False,
            'down': False,
        }
        self.taskAsyncio = {
            'up': None,
            'down': None,
        }
        self.colorArray = [
            "0xE21E59",
            "0x1598E9",
            "0x2FD661",
            "0xF19705",
        ]
        self.color = self.colorArray[self.id]
        self.isAI = False
        self.aiTask = None

    def moveUp(self):
        self.position -= self.speed
    
    def moveDown(self):
        self.position += self.speed

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

    def checkPaddleCollision(self, paddle):
        # TODO a voir si on inverse pas des le debut plutot que inverser chaque fois
        if (paddle.id == 2 or paddle.id == 3):
            paddleThickness, paddleSize = paddle.paddleSize, paddle.paddleThickness
            offset, position = paddle.position, paddle.offset
        else:
            paddleThickness, paddleSize = paddle.paddleThickness, paddle.paddleSize
            offset, position = paddle.offset, paddle.position

        closestX = max(offset, min(self.x, offset + paddleThickness))
        closestY = max(position, min(self.y, position + paddleSize))
        distance = math.sqrt((self.x - closestX)**2 + (self.y - closestY)**2)

        if distance < self.radius:
            print("collisions paddle : ", paddle.id)

    def checkWallCollision(self, gameSettings):
        id = -1
        if (self.x <= 0):
            self.angle = math.pi - self.angle
            id = 0
        elif (self.x >= gameSettings.squareSize):
            self.angle = math.pi - self.angle
            id = 1

        # TODO add id to check if wall is collide (update score)
        if (self.y <= 0) or (self.y >= gameSettings.squareSize):
            self.angle = -self.angle
        return (id);

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
        self.angle = random.choice([0, math.pi]) - math.pi / 2