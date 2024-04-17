from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.core.validators import MaxValueValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", 'admin')

        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(email, password, **extra_fields)




class CustomUser(AbstractUser):
    USER_ROLES= (
        ('user','User'),
        ('guide','Guide'),
        ('admin','Admin'),
    )
    profile_image = models.ImageField(upload_to='profile_pics',blank=True,null=True)
    phone = models.CharField(blank=True,null=True,max_length=10)   
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='user')
    address = models.TextField(blank=True,null=True)
    is_google = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['username']
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email