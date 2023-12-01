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
        closest_x = max(self.x, min(ball.x, self.x + self.width))
        closest_y = max(self.y, min(ball.y, self.y + self.height))

        distance = math.sqrt((ball.x - closest_x)**2 + (ball.y - closest_y)**2)

        if distance <= ball.radius:
            return True
        return False

class Ball:
    def __init__(self):
        self.x = 100.0
        self.y = 100.0
        self.radius = 8
        self.speed = 10
        self.angle = 1.0
        self.task = None

    def checkCollision(self, paddle):
        closest_x = max(paddle.x, min(self.x, paddle.x + paddle.width))
        closest_y = max(paddle.y, min(self.y, paddle.y + paddle.height))

        # Calculer la distance entre le centre du cercle et le point le plus proche sur le rectangle
        distance = math.sqrt((self.x - closest_x)**2 + (self.y - closest_y)**2)

        # Vérifier si la distance est inférieure ou égale au rayon du cercle
        return distance <= self.radius

    def move(self):
        deltaX = self.speed * math.cos(self.angle) 
        deltaY = self.speed * math.sin(self.angle)
        self.x += deltaX
        self.y += deltaY