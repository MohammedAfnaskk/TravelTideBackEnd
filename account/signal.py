from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from .utils import send_activation_email

@receiver(post_save,sender=CustomUser)
def user_activation(sender, instance,created, **kwargs):
    if created:
        send_activation_email(
            instance
        )