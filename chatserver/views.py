from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import CreateAPIView,ListAPIView,ListCreateAPIView

from account.models import CustomUser
from .serializers import ChatListSerializer, MessageSerializer
from .models import Message
from rest_framework.filters import SearchFilter
 

class ChatCreatingView(CreateAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


class PreviousMessagesView(ListAPIView):
    serializer_class = MessageSerializer
    pagination_class = None

    def get_queryset(self):
        user1 = int(self.kwargs['user1'])
        user2 = int(self.kwargs['user2'])

        thread_suffix = f"{user1}_{user2}" if user1 > user2 else f"{user2}_{user1}"
        thread_name = 'chat_'+thread_suffix
        queryset = Message.objects.filter(
            thread_name=thread_name
        )
        return queryset
 
 

# class SingleUserChatsView(ListAPIView):
#     serializer_class = ChatSerializer 
    
#     def get(self, request, *args, **kwargs):
#         userID = self.kwargs['id']
#         user = CustomUser.objects.get(id=userID)
#         chat_count = Message.objects.filter(sender=user).union(Message.objects.filter(receiver=user)).count()
#         return Response({"chat_count": chat_count}, status=status.HTTP_200_OK)



class ChatListUsers(ListAPIView):
    serializer_class = ChatListSerializer
    def get_queryset(self):
        current_user_id = self.request.user.id

        # Get distinct users with whom the current user has had chats
        chat_users = Message.objects.filter(sender_id=current_user_id).values_list('receiver', flat=True).distinct()

        # Return the queryset of chat users
        return CustomUser.objects.filter(id__in=chat_users)
    def list(self, request, *args, **kwargs):
 
        # Get distinct users with whom the current user has had chats
        sender_users = Message.objects.filter(sender_id=current_user_id).values_list('receiver', flat=True).distinct()
        receiver_users = Message.objects.filter(receiver_id=current_user_id).values_list('sender', flat=True).distinct()
        chat_users = set(sender_users).union(receiver_users)

        # Get user details for each chat user
        users_data = []
        for user_id in chat_users:
            user_data = {
                'id': user_id,
                'username': CustomUser.objects.get(id=user_id).username,
                'email': CustomUser.objects.get(id=user_id).email,
                # Add other fields you need
            }
            users_data.append(user_data)

        return Response(users_data, status=status.HTTP_200_OK)