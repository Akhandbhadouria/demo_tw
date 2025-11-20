from django.urls import path
from . import views

urlpatterns = [
    path('start/<str:username>/', views.start_chat, name='start_chat'),  # Start chat with user
    path('room/<int:chatroom_id>/', views.chat_room, name='chat_room'),  # View chat room
        path('inbox/', views.inbox, name='inbox'),

  
 path('chat/delete/<int:room_id>/', views.delete_chat, name='delete_chat'),

path('message/delete/<int:msg_id>/', views.delete_message, name='delete_message'),
]
