from django.urls import path
from . import views

urlpatterns = [
    path("chat/", views.chat, name="chat"),
    path("chat/<str:room_name>/", views.room, name="room"),
    path("create_channel/<str:user_to>/", views.create_channel, name="create_channel")
]
