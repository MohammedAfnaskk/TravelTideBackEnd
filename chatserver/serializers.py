from rest_framework.serializers import ModelSerializer

from account.models import CustomUser
from .models import Message
from rest_framework import serializers
from django.urls import reverse
from django.http import request

class MessageSerializer(ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email')

    class Meta:
        model = Message
        fields = ['message', 'sender_email']

 
 
 
 