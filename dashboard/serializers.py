from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from account.models import CustomUser
from travel_manager.models import MainPlace, TripPlanning
from .models import *



class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        token['role'] = user.role
        token['is_admin'] = user.is_superuser
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


# Block UnBlock Serializer
class BlockUnblockSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['is_active']
        
# User List Search  Serializer
class UsersListSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ('password',)

 