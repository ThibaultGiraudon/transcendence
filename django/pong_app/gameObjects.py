class Paddle:
    def __init__(self, id):
        self.id = id
        self.position = 0
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
        self.position -= self.speed
    
    def moveDown(self):
        self.position += self.speed

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
