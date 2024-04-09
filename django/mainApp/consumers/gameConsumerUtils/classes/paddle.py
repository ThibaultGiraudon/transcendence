class Paddle:
    def __init__(self, id):
        self.id = id
        self.offset = 0
        self.position = 0
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
            "#E21E59",
            "#1598E9",
            "#2FD661",
            "#F19705",
        ]
        self.color = self.colorArray[self.id]
        self.isAlive = False
        self.isAI = False
        self.aiTask = None
        self.rankPosition = 0

    def moveUp(self):
        self.position -= self.speed
    
    def moveDown(self):
        self.position += self.speed