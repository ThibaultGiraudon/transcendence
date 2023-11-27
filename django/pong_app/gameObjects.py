class Paddle:
    def __init__(self, name):
        self.name = name
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

    # def move_up(self, step):
    #     self.y -= step

    # def move_down(self, step):
    #     self.y += step


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
