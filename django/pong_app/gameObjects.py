import math

class GameSettings:
    def __init__(self, nbPaddles, width, height):
        self.nbPaddles = nbPaddles
        self.gameWidth = width
        self.gameHeight = height
        self.paddles = []
        self.ball = Ball()

        for id in range(self.nbPaddles):
            self.paddles.append(Paddle(id))
    
    def resetPaddles(self):
        for paddle in self.paddles:
            # TODO change maybe
            paddle.y = self.gameHeight / 2 - 50

class Paddle:
    def __init__(self, id):
        self.id = id
        self.x = 0
        self.y = 0
        self.width = 20
        self.height = 100
        self.speed = 20
        self.keyState = {
            'up': False,
            'down': False,
        }
        self.taskAsyncio = {
            'up': None,
            'down': None,
        }

    def moveUp(self):
        self.y -= self.speed
    
    def moveDown(self):
        self.y += self.speed

class Ball:
    def __init__(self):
        self.x = 100.0
        self.y = 100.0
        self.radius = 8
        self.speed = 20
        self.angle = 1.0
        self.task = None

    def checkPaddleCollision(self, paddle):
        closestX = max(paddle.x, min(self.x, paddle.x + paddle.width))
        closestY = max(paddle.y, min(self.y, paddle.y + paddle.height))
        distance = math.sqrt((self.x - closestX)**2 + (self.y - closestY)**2)

        if (distance <= self.radius):
            collisionPosition = (closestY - paddle.y) / paddle.height
            reflectionAngle = (collisionPosition - 0.5) * math.pi
            maxAngle = math.pi / 3

            if (paddle.id == 0):
                self.angle = max(-maxAngle, min(maxAngle, reflectionAngle))
            elif (paddle.id == 1):
                self.angle = math.pi - max(-maxAngle, min(maxAngle, reflectionAngle))

            speedFactor = 1 - abs(collisionPosition - 0.5)
            self.speed = 20 * speedFactor * 1.5

    def checkWallCollision(self, gameSettings):
        if (self.x <= 0) or (self.x >= gameSettings.gameWidth):
            self.angle = math.pi - self.angle
        if (self.y <= 0) or (self.y >= gameSettings.gameHeight):
            self.angle = -self.angle

    def move(self):
        deltaX = self.speed * math.cos(self.angle) 
        deltaY = self.speed * math.sin(self.angle)
        self.x += deltaX
        self.y += deltaY