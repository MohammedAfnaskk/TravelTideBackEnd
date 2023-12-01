from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets

from travel_manager.models import MainPlace
from travel_manager.serializers import MainPlaceSerializer
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView,CreateAPIView, ListCreateAPIView, UpdateAPIView,ListAPIView
from rest_framework import generics
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination


class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer
# Guide Details
class GuideDetailsView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        return CustomUser.objects.filter(role='guide')
 
# Guide Block Unblock
class GuideBlockUnblock(UpdateAPIView):
    queryset = CustomUser.objects.all().exclude(is_superuser=True)
    serializer_class = BlockUnblockSerializer
    lookup_field = 'id'

# User Details
class UserDetailsView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        return CustomUser.objects.filter(role='user')
 
# User Block Unblock
class UserBlockUnblock(UpdateAPIView):
    queryset = CustomUser.objects.all().exclude(is_superuser=True)
    serializer_class = BlockUnblockSerializer
    lookup_field = 'id'


#Trip Place and Budget Chart
class MainPlaceData(APIView):
    def get(self, request, *args, **kwargs):
        places = MainPlace.objects.all()
        serializer = MainPlaceSerializer(places, many=True)
        return Response(serializer.data)
    

# Active User and join Date 
class ActiveUsersGuideCountView(APIView):
    def get(self, request, *args, **kwargs):
        # Count active users and guides based on join date
        active_users_count_by_date = (
            CustomUser.objects
            .filter(is_active=True, role='user')
            .annotate(join_date=TruncDate('date_joined'))
            .values('join_date')
            .annotate(count=Count('id'))
        )

        active_guides_count_by_date = (
            CustomUser.objects
            .filter(is_active=True, role='guide')
            .annotate(join_date=TruncDate('date_joined'))
            .values('join_date')
            .annotate(count=Count('id'))
        )

        # Return data as JSON
        data = {
            'active_users_count_by_date': list(active_users_count_by_date),
            'active_guides_count_by_date': list(active_guides_count_by_date),
        }

        return JsonResponse(data)
    

# User List Search
class UsersList(ListAPIView):
    serializer_class = UsersListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'role']
    pagination_class = PageNumberPagination
    queryset = CustomUser.objects.filter(role='user').exclude(is_superuser=True).order_by('-id')

# User List Search
class GuideList(ListAPIView):
    serializer_class = UsersListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'role']
    pagination_class = PageNumberPagination
    queryset = CustomUser.objects.filter(role='guide').exclude(is_superuser=True).order_by('-id')


 