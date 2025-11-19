from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import ChatRoom, Message
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required #login_required is used to restrict access to a view so that only authenticated (logged-in) users can access it.

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import ChatRoom, Message

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import ChatRoom

@login_required
def get_or_create_room(request, username):
    user1 = request.user
    user2 = get_object_or_404(User, username=username)

    # Ensure user2 is followed by user1 (optional safety check)
    if not user2.userprofile.followers.filter(id=user1.id).exists():
        # Redirect back with a message or raise 404
        return redirect('following_feed')

    # Check if room already exists
    room = ChatRoom.objects.filter(users=user1).filter(users=user2).first()

    if not room:
        room = ChatRoom.objects.create()
        room.users.add(user1, user2)

    return redirect("chat_room", room.id)

from django.shortcuts import render, get_object_or_404, redirect
from .models import ChatRoom, Message
from django.contrib.auth.decorators import login_required
@login_required
def chat_room(request, chatroom_id):
    chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
    messages = chatroom.messages.all().order_by('timestamp')
    
    # Get the other participant
    other_user = chatroom.participants.exclude(id=request.user.id).first()

    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            chatroom.messages.create(sender=request.user, content=content)
            return redirect('chat_room', chatroom_id=chatroom.id)

    return render(request, 'chat/chat_room.html', {
        'chatroom': chatroom,
        'messages': messages,
        'other_user': other_user
    })


from django.shortcuts import get_object_or_404, redirect
from .models import ChatRoom
from django.contrib.auth.models import User
@login_required
def start_chat(request, username):
    other_user = get_object_or_404(User, username=username)
    user = request.user

    # Check if a ChatRoom already exists for these two users
    chatroom = ChatRoom.objects.filter(participants=user).filter(participants=other_user).first()
    
    if not chatroom:
        chatroom = ChatRoom.objects.create()
        chatroom.participants.add(user, other_user)

    return redirect('chat_room', chatroom_id=chatroom.id)


# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import models  # Add this import
from .models import ChatRoom, Message  # Make sure you have this import
from django.utils import timezone  # Add this for timezone handling
from django.http import HttpResponseForbidden  # Import for forbidden response

@login_required
def inbox(request):
    # Get all chatrooms where current user is a participant
    chatrooms = ChatRoom.objects.filter(participants=request.user).annotate(
        last_message_time=models.Max('messages__timestamp')
    ).order_by('-last_message_time', '-created_at')

    # For each chatroom, find the other participant(s) and get message info
    conversations = []
    for room in chatrooms:
        other_user = room.participants.exclude(id=request.user.id).first()
        if other_user:
            # Get the last message in this chatroom
            last_message = room.messages.order_by('-timestamp').first()
            
            # Count unread messages (messages after user's last login)
            unread_count = room.messages.filter(
                sender=other_user,
                timestamp__gt=request.user.last_login
            ).count() if request.user.last_login else room.messages.filter(sender=other_user).count()
            
            conversations.append({
                'chatroom': room,
                'user': other_user,
                'last_message': last_message,
                'unread_count': unread_count
            })

    return render(request, 'chat/inbox.html', {'conversations': conversations})


@login_required
def delete_chat(request, room_id):
    chatroom = get_object_or_404(ChatRoom, id=room_id)

    # Allow deletion only if the user is part of the chatroom
    if request.user not in chatroom.participants.all():
        return HttpResponseForbidden("You cannot delete this chat.")

    # Delete all messages and chatroom
    chatroom.delete()

    return redirect('inbox')  # Your message inbox page
@login_required
def delete_message(request, msg_id):
    message = get_object_or_404(Message, id=msg_id)

    # Only the sender can delete their message
    if message.sender != request.user:
        return HttpResponseForbidden("You can delete only your messages.")

    chatroom_id = message.chatroom.id  # <-- correct field

    message.delete()

    return redirect('chat_room', chatroom_id=chatroom_id)
