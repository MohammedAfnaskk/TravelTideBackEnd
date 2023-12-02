from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
   path ('create-checkout-session',Payment.as_view()),
  
   
]