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
        self.width = 10
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
    
    def checkCollision(self, ball):
        if (
            ball.x >= self.x and
            ball.x <= self.x + 10 and
            ball.y >= self.y and
            ball.y <= self.y + 100
        ):
            return True
        return False

class Ball:
    def __init__(self):
        self.x = 100.0
        self.y = 100.0
        self.radius = 10
        self.speed = 10
        self.angle = 1.0
        self.task = None

    def move(self):
        deltaX = self.speed * math.cos(self.angle) 
        deltaY = self.speed * math.sin(self.angle)
        self.x += deltaX
        self.y += deltaY