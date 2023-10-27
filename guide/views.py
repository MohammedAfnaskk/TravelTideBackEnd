from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

 

User = get_user_model()

class GuideGoogleAuthendication(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not User.objects.filter(email=email,is_google=True).exists():
            serializer = GuideGoogleAuthSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):   
                user = serializer.save()
                user.is_active = True
                user.is_google = True
                user.role = 'guide'
                user.set_password(password)
                user.save()
        user = authenticate( email=email, password=password)
        if user is not None:    
            token=create_jwt_pair_tokens(user)
            response_data = {
                'status': 'success',
                'msg': 'Registratin Successfully',
                'token': token,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'error', 'msg': serializer.errors})
        




def create_jwt_pair_tokens(user):
    refresh = RefreshToken.for_user(user)
    refresh['username'] = user.username
    refresh['email'] = user.email
    refresh['role'] = user.role
    refresh['is_active'] = user.is_active
    refresh['is_admin'] = user.is_superuser

    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    return {
        "access": access_token,
        "refresh": refresh_token,
    }
