from django.conf import settings
from rest_framework.views import APIView
import stripe
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
import logging
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from travel_manager.serializers import MainPlaceSerializer
from .models import *
from .serializers import StripPaymentSerializer
from rest_framework import generics, permissions
from datetime import datetime
from datetime import date
from rest_framework import viewsets

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

def get_user_role(user_id):
     
    try:
        user = CustomUser.objects.get(id=user_id)
        return user.role
    except CustomUser.DoesNotExist:
        return None 
    

    

class Payment(APIView):
    def post(self, request):
        try:
            trip_id = request.data.get('trip_id')
            main_place = request.data.get('main_place')
            budget = request.data.get('budget')
            image = request.data.get('image')
            print(f"Image URL: {image}")

            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'INR',
                        'product_data': {
                            'name': main_place,
                            'images': [image],  # Add the image URL here
                        },
                        'unit_amount': budget * 100,
                    },
                    'quantity': 1,
                }],
                # Change this to the appropriate payment method type
                payment_method_types=['card'],
                mode="payment",
                success_url = f"https://traveltide.vercel.app/user/trip-package-details/{trip_id}/?success=true&session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"https://traveltide.vercel.app/user/trip-package-details/{trip_id}/?canceled=true",
            )

            return Response({
                'message': {
                    'url': checkout_session.url,
                    'image_url': image,
                }
            })
        except Exception as e:
            # Log the exception for debugging purposes
            print(f"Error creating checkout session: {e}")
            return Response({'error': 'An error occurred while creating the checkout session'}, status=500)


class StripPaymentViewSet(viewsets.ModelViewSet):
    queryset = StripPayment.objects.all()
    serializer_class = StripPaymentSerializer

    def perform_create(self, serializer):
        # Check if the payment record already exists for the given user and trip
        existing_payment = StripPayment.objects.filter(
            user=serializer.validated_data['user'],
            trip=serializer.validated_data['trip'],
        ).first()

        if existing_payment:
            # If the record already exists, update it instead of creating a new one
            existing_payment.payment = serializer.validated_data['payment']
            existing_payment.payment_date = date.today()
            existing_payment.save()
            serializer.instance = existing_payment
        else:
            # If the record doesn't exist, create a new one
            serializer.save(payment_date=date.today())

    def perform_update(self, serializer):
        if 'payment' in self.request.data and self.request.data['payment']:
            # Check if the payment record already exists for the given user and trip
            existing_payment = StripPayment.objects.filter(
                user=serializer.validated_data['user'],
                trip=serializer.validated_data['trip'],
            ).first()

            if existing_payment:
                # If the record already exists, update it
                existing_payment.payment = serializer.validated_data['payment']
                existing_payment.payment_date = date.today()
                existing_payment.save()
                serializer.instance = existing_payment
            else:
                # If the record doesn't exist, perform the regular update
                serializer.save(payment_date=date.today())
        else:
            serializer.save()


class PaymentDetailsView(generics.RetrieveAPIView):
    serializer_class = StripPaymentSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        trip_id = self.kwargs['trip_id']
        payment = StripPayment.objects.filter(
            user=user_id, trip=trip_id).first()
        return payment

    

class UserPaymentDetailsView(generics.ListAPIView):
    serializer_class = StripPaymentSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user_role = get_user_role(user_id)

        if user_role == 'user':
            return StripPayment.objects.filter(user=user_id)
        elif user_role == 'guide':
            return StripPayment.objects.filter(trip__user_id=user_id)
        else:
            return StripPayment.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        for payment_data in data:
            trip_id = payment_data['trip']

            try:
                trip_instance = MainPlace.objects.get(pk=trip_id)
                trip_serializer = MainPlaceSerializer(trip_instance)
                payment_data['trip_details'] = trip_serializer.data
            except MainPlace.DoesNotExist:
                payment_data['trip_details'] = None

        return Response(data)


class AllPaymentDetailsView(generics.ListAPIView):
    serializer_class = StripPaymentSerializer

    def get_queryset(self):
        return StripPayment.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        for payment_data in data:
            trip_id = payment_data['trip']

            try:
                trip_instance = MainPlace.objects.get(pk=trip_id)
                trip_serializer = MainPlaceSerializer(trip_instance)
                payment_data['trip_details'] = trip_serializer.data
            except MainPlace.DoesNotExist:
                payment_data['trip_details'] = None

        return Response(data)
    
 