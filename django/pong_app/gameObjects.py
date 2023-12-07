import math
import random

class GameSettings:
    def __init__(self, nbPaddles, width, height):
        self.nbPaddles = nbPaddles
        self.gameWidth = width
        self.gameHeight = height
        self.paddles = []
        self.ball = Ball()

        for id in range(self.nbPaddles):
            self.paddles.append(Paddle(id))
        
        if self.nbPaddles == 2:
            self.initPaddles2()
        elif self.nbPaddles == 4:
            self.initPaddles4()
    
    def resetPaddles(self):
        for paddle in self.paddles:
            # TODO change maybe
            paddle.y = self.gameHeight / 2 - 50
    
    def initPaddles2(self):
        self.paddles[0].x = 10
        self.paddles[1].x = self.gameWidth - self.paddles[1].width - 10

    def initPaddles4(self):
        self.paddles[0].x = 10
        self.paddles[1].x = self.gameWidth - self.paddles[1].width - 10
        self.paddles[2].y = 10
        self.paddles[3].y = self.gameHeight - self.paddles[3].width - 10

        self.paddles[2].width, self.paddles[2].height = self.paddles[2].height, self.paddles[2].width
        self.paddles[3].width, self.paddles[3].height = self.paddles[3].height, self.paddles[3].width

class Paddle:
    def __init__(self, id):
        self.id = id
        self.x = 0
        self.y = 0
        self.width = 20
        self.height = 100
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

    def moveUp(self):
        self.y -= self.speed
    
    def moveDown(self):
        self.y += self.speed

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
        closestX = max(paddle.x, min(self.x, paddle.x + paddle.width))
        closestY = max(paddle.y, min(self.y, paddle.y + paddle.height))
        distance = math.sqrt((self.x - closestX)**2 + (self.y - closestY)**2)

        if (distance <= self.radius):
            collisionPosition = (closestY - paddle.y) / paddle.height
            reflectionAngle = (collisionPosition - 0.5) * math.pi
            maxAngle = math.pi / 3

            print("collision paddle")

            if (paddle.id == 0):
                self.angle = max(-maxAngle, min(maxAngle, reflectionAngle))
            elif (paddle.id == 1):
                self.angle = math.pi - max(-maxAngle, min(maxAngle, reflectionAngle))

            self.__powerShot(paddle, collisionPosition)

    def checkWallCollision(self, gameSettings):
        id = -1
        if (self.x <= 0):
            self.angle = math.pi - self.angle
            id = 0
        elif (self.x >= gameSettings.gameWidth):
            self.angle = math.pi - self.angle
            id = 1

        if (self.y <= 0) or (self.y >= gameSettings.gameHeight):
            self.angle = -self.angle
        return (id);

    def move(self):
        deltaX = self.speed * math.cos(self.angle) 
        deltaY = self.speed * math.sin(self.angle)
        self.x += deltaX
        self.y += deltaY

    def resetBall(self, gameSettings):
        self.x = gameSettings.gameWidth / 2
        self.y = gameSettings.gameHeight / 2
        self.radius = 10
        self.color = "0xFDF3E1"
        self.speed = 5
        self.angle = random.choice([0, math.pi])