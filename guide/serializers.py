# User Google Account
from rest_framework import serializers
from account.models import CustomUser



class GuideGoogleAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  
        fields = ['id', 'username', 'email', 'password', 'profile_image', 'role', 'is_google']
        extra_kwargs = {
            'password': {'write_only': True}
        }

