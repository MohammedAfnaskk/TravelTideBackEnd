from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
   path ('create-checkout-session',Payment.as_view()),
   path('payment/<int:user_id>/', PaymentDetailsView.as_view(), name='payment-details'),

   
]