from django.urls import path
from .views import *
urlpatterns = [

    path("user-previous-chats/<int:user1>/<int:user2>/", PreviousMessagesView.as_view()),
    path('chatlistusers/', ChatListUsers.as_view(), name='chat-list-users'),

  ]