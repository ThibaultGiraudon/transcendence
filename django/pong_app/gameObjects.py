class GameSettings:
    def __init__(self, nbPaddles):
        self.nbPaddles = nbPaddles
        # TODO change name to game instead of canvas 
        self.canvasWidth = 0
        self.canvasHeight = 0
        self.paddles = []
        self.ball = Ball()

        for id in range(self.nbPaddles):
            self.paddles.append(Paddle(id))
    
    def resetPaddles(self):
        self.paddles.clear()
        # for paddle in self.paddles:
            # paddle.clear()
        for id in range(self.nbPaddles):
            self.paddles.append(Paddle(id))

class Paddle:
    def __init__(self, id):
        self.id = id
        self.x = 0
        self.y = 400
        self.speed = 20
        self.keyState = {
            'up': False,
            'down': False,
        }
        self.taskAsyncio = {
            'up': None,
            'down': None,
        }

    # TODO maybe change to one method move who check collide
    def moveUp(self):
        self.y -= self.speed
    
    def moveDown(self):
        self.y += self.speed
    
    # def checkCollision(self, ball):

class Ball:
    def __init__(self):
        self.x = 100.0
        self.y = 100.0
        self.speed = 10
        self.angle = 1.0
        self.task = None

#     def move(self):
#         delta_x = self.speed * math.cos(self.angle)
#         delta_y = self.speed * math.sin(self.angle)
#         self.x += delta_x
#         self.y += delta_y
