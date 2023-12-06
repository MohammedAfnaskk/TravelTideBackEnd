# serializers.py
from rest_framework import serializers
from .models import StripPayment

class StripPaymentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = StripPayment
        fields = ['id','user', 'user_name', 'trip', 'payment', 'payment_date']
