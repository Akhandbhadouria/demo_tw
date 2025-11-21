from django.urls import path
from . import views

urlpatterns = [
   path('', views.combined_chat_view, name='combined_chat'),
    path('<int:chatroom_id>/', views.combined_chat_view, name='combined_chat'),
    path('start-chat/<str:username>/', views.start_chat, name='start_chat'),
    path('delete-chat/<int:room_id>/', views.delete_chat, name='delete_chat'),
    path('delete-message/<int:msg_id>/', views.delete_message, name='delete_message'),
]
