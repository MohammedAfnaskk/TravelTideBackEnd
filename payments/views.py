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
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": "price_1OIquiSHlmNPAfSJyOHoDs5J",
                        "quantity": 1,
                    },
                ],
                payment_method_types=['card',],
                mode="payment",
                # success_url=f"{
                #     settings.CORS_ALLOWED_ORIGINS[0]}/?success=true&session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=settings.CORS_ALLOWED_ORIGINS[0] +
                '/?canceled=true',
            )

            logger.info(f"Value of checkout_session: {checkout_session}")
            return Response({"message": checkout_session}, status=status.HTTP_200_OK)
        except Exception as e:

            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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