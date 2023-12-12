from django.db import models

class Message(models.Model):
    room = models.CharField(max_length=255)
    message = models.TextField()
    sender = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)