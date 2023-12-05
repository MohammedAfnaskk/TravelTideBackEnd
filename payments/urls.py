from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'strippayments', StripPaymentViewSet, basename='strippayments')

urlpatterns = [
   path('', include(router.urls)),
   path ('create-checkout-session',Payment.as_view()),
   path('payment-details/<int:user_id>/<int:trip_id>/', PaymentDetailsView.as_view(), name='payment-details'),
   path('user-payment-details/<int:user_id>/', UserPaymentDetailsView.as_view(), name='user-payment-details'),
   
]