# serializers.py
from rest_framework import serializers
from .models import *
from rest_framework.serializers import ModelSerializer

 
class TripPlanningSerializer(serializers.ModelSerializer):    
    class Meta:
        model = TripPlanning
        fields = '__all__'

class MainPlaceSerializer(serializers.ModelSerializer):
    trip_planning = TripPlanningSerializer(many=True,required = False)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = MainPlace
        fields = '__all__'
        
class InviteFriendsSerializer(serializers.Serializer):
    email = serializers.EmailField()


class Invite_Serializer(serializers.ModelSerializer):
    tripp = MainPlaceSerializer( source= 'trip')
    class Meta:
        model = Invitation 
        fields =['id','tripp', 'send_to', 'date', 'status']   

class InvitationUpdateSerializer(serializers.Serializer):
    updatedStatus = serializers.CharField()

class InvitationSerializer(serializers.ModelSerializer):
    tripp = MainPlaceSerializer( source= 'trip')
    class Meta:
        model = Invitation
        fields = '__all__' 

 