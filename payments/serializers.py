# serializers.py
from rest_framework import serializers
from .models import StripPayment

class StripPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripPayment
        fields = ['id','user', 'trip', 'payment', 'payment_date']
