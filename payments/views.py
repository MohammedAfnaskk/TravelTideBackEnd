from django.conf import settings
from rest_framework.views import APIView
import stripe
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect 
import logging

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

class Payment(APIView):
    def post(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": "price_1O5PKpSHlmNPAfSJdvurHfnl",
                        "quantity": 1,
                    },
                ],
                payment_method_types=['card',],
                mode="payment",
                success_url=f"{settings.CORS_ALLOWED_ORIGINS[0]}/?success=true&session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=settings.CORS_ALLOWED_ORIGINS[0] + '/?canceled=true',
            )

            logger.info(f"Value of checkout_session: {checkout_session}")
            return Response({ "message" : checkout_session },status= status.HTTP_200_OK)
        except Exception as e:

            return Response({ "message" : str(e)},status= status.HTTP_500_INTERNAL_SERVER_ERROR)
