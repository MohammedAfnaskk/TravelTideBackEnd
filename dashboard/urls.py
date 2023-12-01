from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
  
 

urlpatterns = [
   path('token/',AdminTokenObtainPairView.as_view(), name='AdminTokenObtainPairView'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('guide_details/', GuideDetailsView.as_view(), name='guide_details'),
   path('guideblockunblock/<int:id>/',GuideBlockUnblock.as_view(), name="GuideBlockUnblock"),
   path('user_details/', UserDetailsView.as_view(), name='user_details'),
   path('userblockunblock/<int:id>/',UserBlockUnblock.as_view(), name="GuideBlockUnblock"),
   path('main_place_data/', MainPlaceData.as_view(), name='main_place_data'),
   path('active-users-guide-count/', ActiveUsersGuideCountView.as_view(), name='active_users_guide_count'),
   path('userslist/',UsersList.as_view(), name="UsersList"),
   path('guidelist/',GuideList.as_view(), name="guideList"),
]
