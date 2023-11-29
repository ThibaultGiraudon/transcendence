"""
ASGI config for main project.

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
from    chat_app import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

# TODO change name of url
websocket_urlpatterns = [
    re_path(r'ws/some_path/$', PongConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})