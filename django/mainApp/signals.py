from django.core.signals import request_started
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from mainApp.models import Player

@receiver(request_started)
def create_custom_user(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(id=0).exists():
        try:
            player = Player.objects.create(id=0, currentGameID=None)
            User.objects.create(id=0, username='System Info', password='password', player=player)
        except:
            pass