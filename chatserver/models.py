from django.db import models
from account.models import CustomUser
 
class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,related_name="sender_message_set")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,related_name="reciever_message_set")
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)