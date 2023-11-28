from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from users_app.models import CustomUser
from django.db import models
from .models import Message

@login_required
def chat_room(request, username):
    other_user = get_object_or_404(CustomUser, username=username)
    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(receiver=other_user)) |
        (models.Q(sender=other_user) & models.Q(receiver=request.user))
    ).order_by('timestamp')

    return render(request, 'chat/chat_room.html', {'messages': messages, 'other_user': other_user})

@login_required
def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        receiver_username = request.POST.get('receiver_username')
        receiver = get_object_or_404(CustomUser, username=receiver_username)

        Message.objects.create(sender=request.user, receiver=receiver, content=content)

        return JsonResponse({'status': 'OK'})
