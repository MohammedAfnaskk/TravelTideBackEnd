from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *


class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer