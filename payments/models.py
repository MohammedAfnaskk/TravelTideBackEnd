from django.db import models
from account.models import CustomUser
from travel_manager.models import MainPlace


class StripPayment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='strip_payments')
    trip = models.ForeignKey(MainPlace, on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.BooleanField(default=False)
    payment_date =models.DateField(null=True, blank=True)

 