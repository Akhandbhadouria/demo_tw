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

    # check if room exists
    room = ChatRoom.objects.filter(participants=user1).filter(participants=user2).first()

    if not room:
        room = ChatRoom.objects.create()
        room.participants.add(user1, user2)

    return redirect("chat_room", room.id)

from django.shortcuts import render, get_object_or_404, redirect
from .models import ChatRoom, Message
from django.contrib.auth.decorators import login_required


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

    return redirect('combined_chat', chatroom_id=chatroom.id)


# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import models  # Add this import
from .models import ChatRoom, Message  # Make sure you have this import
from django.utils import timezone  # Add this for timezone handling
from django.http import HttpResponseForbidden  # Import for forbidden response


@login_required
def delete_chat(request, room_id):
    chatroom = get_object_or_404(ChatRoom, id=room_id)

    # Allow deletion only if the user is part of the chatroom
    if request.user not in chatroom.participants.all():
        return HttpResponseForbidden("You cannot delete this chat.")

    # Delete all messages and chatroom
    chatroom.delete()

    return redirect('combined_chat')  # Your message inbox page

@login_required
def delete_message(request, msg_id):
    message = get_object_or_404(Message, id=msg_id)

    # Only the sender can delete their message
    if message.sender != request.user:
        return HttpResponseForbidden("You can delete only your messages.")

    chatroom_id = message.chatroom.id

    message.delete()

    # Redirect to combined chat view with the correct URL name
    return redirect('combined_chat', chatroom_id=chatroom_id)



from django.shortcuts import render, get_object_or_404
from .models import ChatRoom, Message
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def combined_chat_view(request, chatroom_id=None):
    # Get all conversations for the inbox
    chatrooms = ChatRoom.objects.filter(participants=request.user).annotate(
        last_message_time=models.Max('messages__timestamp')
    ).order_by('-last_message_time', '-created_at')

    conversations = []
    for room in chatrooms:
        other_user = room.participants.exclude(id=request.user.id).first()
        if other_user:
            last_message = room.messages.order_by('-timestamp').first()
            
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

    # Get active chatroom and messages
    active_chatroom = None
    messages = []
    other_user = None
    
    if chatroom_id:
        active_chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
        # Check if user is participant
        if request.user not in active_chatroom.participants.all():
            return HttpResponseForbidden("You don't have access to this chat.")
        
        messages = active_chatroom.messages.all().order_by('timestamp')
        other_user = active_chatroom.participants.exclude(id=request.user.id).first()

    # Handle message sending - FIX THIS PART
    if request.method == 'POST' and active_chatroom:
        content = request.POST.get('message')
        if content:
            active_chatroom.messages.create(sender=request.user, content=content)
            # Redirect to the same chatroom using the correct URL name
            return redirect('combined_chat', chatroom_id=active_chatroom.id)

    return render(request, 'chat/combine.html', {
        'conversations': conversations,
        'active_chatroom': active_chatroom,
        'messages': messages,
        'other_user': other_user
    })