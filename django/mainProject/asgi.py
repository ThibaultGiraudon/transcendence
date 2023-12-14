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

from    mainApp.consumers.pongConsumer import PongConsumer
from    mainApp.consumers.notificationsConsumer import NotificationConsumer
from    chat_app.consumers import *
from    users_app.consumers import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainProject.settings')

# TODO change name of url
websocket_urlpatterns = [
    re_path(r'ws/some_path/$', PongConsumer.as_asgi()),
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<room_name>[\w-]+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/status/$", StatusConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})