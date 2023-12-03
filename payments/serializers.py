from rest_framework import serializers
from account.models import CustomUser

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','email','payment', 'payment_date']
