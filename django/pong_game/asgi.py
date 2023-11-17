"""
ASGI config for pong_game project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import  os

from    django.core.asgi import get_asgi_application
from    channels.routing import ProtocolTypeRouter, URLRouter
from    channels.auth import AuthMiddlewareStack
from    django.urls import re_path
from    pong_app.consumers import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pong_game.settings')

# TODO change port
websocket_urlpatterns = [
    re_path(r'ws/some_path/$', PongConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})