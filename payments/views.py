from django.conf import settings
from rest_framework.views import APIView
import stripe
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
import logging
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from account.models import CustomUser
from .serializers import PaymentSerializer
from rest_framework import generics, permissions
from datetime import datetime

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


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
                payment_method_types=['card'],  # Change this to the appropriate payment method type
                mode="payment",
                success_url=f"{settings.CORS_ALLOWED_ORIGINS[0]}/user/trip-package-details/{trip_id}/?success=true&session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.CORS_ALLOWED_ORIGINS[0]}/user/trip-package-details/{trip_id}/?canceled=true",
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



class PaymentDetailsView(generics.RetrieveUpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = CustomUser.objects.all()  # Replace with your actual user model

    def get_object(self):
        user_id = self.kwargs.get('user_id') 
        return self.queryset.get(pk=user_id)
    def update_payment_status(self, user, payment, payment_date):
        user.payment = payment

        # Parse the date string to a datetime object
        if payment_date:
            user.payment_date = datetime.fromisoformat(payment_date)

        user.save()


    def patch(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')  # Assuming 'user_id' is passed in URL parameters
        user = self.get_object()

        payment_success = request.data.get('payment', False)
        payment_date = request.data.get('payment_date', None)

        # Update user payment status and date
        self.update_payment_status(user, payment_success, payment_date)

        return Response({"success": True, "message": "Payment status updated successfully"})