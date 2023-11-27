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


# class Ball:
#     def __init__(self, x, y, speed, angle):
#         self.x = x
#         self.y = y
#         self.speed = speed
#         self.angle = angle

#     def move(self):
#         delta_x = self.speed * math.cos(self.angle)
#         delta_y = self.speed * math.sin(self.angle)
#         self.x += delta_x
#         self.y += delta_y
