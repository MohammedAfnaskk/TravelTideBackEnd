from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.core.validators import MaxValueValidator

 
class CustomUser(AbstractUser):
    USER_ROLES= (
        ('user','User'),
        ('guide','Guide'),
        ('admin','Admin'),
    )
    
    email = models.EmailField(unique=True)
    password =models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profile_pics',blank=True,null=True)
    phone = models.PositiveIntegerField(blank=True,null=True)    
    role = models.CharField(max_length=10, choices=USER_ROLES, default='user')
    address = models.TextField(blank=True,null=True)
    is_google = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    