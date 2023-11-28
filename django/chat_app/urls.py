from django.urls import path
from .views import chat_room, send_message

urlpatterns = [
    path('chat/<str:username>/', chat_room, name='chat_room'),
    path('send_message/', send_message, name='send_message'),
]
