from django.conf import settings
from rest_framework.views import APIView
import stripe
from rest_framework.response import Response
from rest_framework import status
 

stripe.api_key = settings.STRIPE_SECRET_KEY

class Payment(APIView):
    def post(self, request):
        try:
            session = stripe.checkout.Session.create(
                line_items=[
                    {
                         'price': 'price_1O5PKpSHlmNPAfSJdvurHfnl',
                        'quantity': 1,
                    },
                ],
               mode='payment',
               success_url=settings.CORS_ALLOWED_ORIGINS + '/?success=true',
               cancel_url=settings.CORS_ALLOWED_ORIGINS + '/?canceled=true',
            )

            return Response({ "message" : session },status= status.HTTP_200_OK)
        except Exception as e:
           return Response({ "message" : str(e)},status= status.HTTP_500_INTERNAL_SERVER_ERROR)