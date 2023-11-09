from django.db import models

Class	PongBall(models.Model):
	x = models.IntegerField()
	y = models.IntegerField()

Class	PongPaddle(models.Model):
	x = models.IntegerField()
	y = models.IntegerField()