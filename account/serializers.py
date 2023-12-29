from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re
 


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username', 'email', 'password','role','profile_image','phone','address']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
# User Google Account
class GoogleAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  
        fields = ['id', 'username', 'email', 'password', 'profile_image', 'role', 'is_google']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
 
        
# Token
class myTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):      
        token = super().get_token(user)
        token['username']=user.username
        token['email'] = user.email
        token['role'] = user.role
        token['is_active'] = user.is_active
        token['is_admin'] = user.is_superuser
        return token
   
    
        
        
        
        
        
