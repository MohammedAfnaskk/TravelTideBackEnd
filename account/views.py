from .serializers import  UserSerializer,myTokenObtainPairSerializer,GoogleAuthSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import RetrieveUpdateDestroyAPIView,CreateAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .models import *
from django.shortcuts import redirect
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from rest_framework import status
from django.shortcuts import HttpResponseRedirect
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from django.contrib.sites.models import Site
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from decouple import config
from account.tasks import *
from .utils import send_activation_email

User = get_user_model()
 
 

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = myTokenObtainPairSerializer


class UserRegistration(CreateAPIView):
    def get_serializer_class(self):
        return UserSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            user.set_password(password)
            user.save()
 
            send_activation_email(user)

            response_data = {
                'status': 'success',
                'msg': 'A verification link sent to your registered email address',
                'data': serializer.data
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            print('Serializer errors are:', serializer.errors)
            return Response({'status': 'error', 'msg': serializer.errors})
 
    
class UserActivationView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)

                
            if user is not None and default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                message = 'Congrats! Account activated!'
                if user.role == 'user':
                    redirect_url = config|()+ '?message=' + message
                else:
                    redirect_url =  + '?message=' + message
                    
            else:
                message = 'Invalid activation link'
                redirect_url =  + '?message=' + message

            return HttpResponseRedirect(redirect_url)
        except Exception as e:
            return Response({'message': 'Activation Failed'}, status=status.HTTP_400_BAD_REQUEST)



# Resend Registration mail
@api_view(['POST'])
def Resend_registration_link(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email = email)
        if user:
            send_activation_email(email, user.pk)
        response_data = {
                'status': 'success',
                'msg': 'A verification link sent to your registered email address',
            }
        return Response(response_data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': 'invalid email'}, status=status.HTTP_404_NOT_FOUND)


# Google Signup
class GoogleAuthendication(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not User.objects.filter(email=email,is_google=True).exists():
            serializer = GoogleAuthSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):

                user = serializer.save()
                user.is_active = True
                user.is_google = True
                user.role = 'user'
                user.set_password(password)
                user.save()
        user = authenticate( email=email, password=password)

        if user is not None:
            token=create_jwt_pair_tokens(user)
            response_data = {
                'status': 'success',
                'msg': 'Registration Successfully',
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
 
# Forgot password
class Forgotpassword(APIView):
    def post(self, request):
        email =  request.data.get('email')
        if CustomUser.objects.filter(email=email).exclude(is_google=True).exists():
            user = User.objects.get(email__exact=email)
            current_site = get_current_site(request)
            domain = current_site.domain.rstrip('/')

            mail_subject = 'Click this link to change your password'
            message = render_to_string('user/forgot_password.html',{
                'user' : user,
                'domain' : domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
                'site' : domain
            })
            to_email = email
            send_mail = EmailMessage(mail_subject,message,to=[to_email])
            send_mail.send()           
            print(f'UID: {urlsafe_base64_encode(force_bytes(user.pk))}')
            print(f'Token: {default_token_generator.make_token(user)}')
            return Response(data={'message' : 'verification email has been sent to your email address','user_id' : user.id,},status=status.HTTP_200_OK)
        else:
            return Response(data={'message' : 'No account found'},status=status.HTTP_404_NOT_FOUND)

# Forgot password password changeing section
@api_view(['GET'])
def resetpassword(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    Baseurl = config('BaseUrl', default='http://localhost:5173/')
    if user is not None and default_token_generator.check_token(user,token):
        redirect_url = f'{Baseurl}resetpassword/?key={uidb64}/?t={token}/'
    else:
        message = 'Invalid activation link'
        redirect_url = f'{Baseurl}resetpassword' + '?message=' + message
    return HttpResponseRedirect(redirect_url)

# Update User Details   
class ResetPassword(APIView):
    def post(self, request,uidb64, format=None):
        password = request.data.get('password')
        if uidb64 and password:  
            try:
                user_id = urlsafe_base64_decode(uidb64).decode()
                user = CustomUser.objects.get(id=user_id)
                
              
                user.set_password(password)
                user.save()
                return Response(data={'message': 'Password has been reset successfully'})
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
 
                return Response(data={'message': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'message': 'Token or password not provided'}, status=status.HTTP_400_BAD_REQUEST)

class GuideDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'id'
    parser_classes = [MultiPartParser, FormParser]

