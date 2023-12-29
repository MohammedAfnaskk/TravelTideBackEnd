from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from .import views
 
urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',UserRegistration.as_view(),name="user_register"),
    path('activate/<str:uidb64>/<str:token>/', UserActivationView.as_view(), name='activate'),
    path('Resend_registration_link/', views.Resend_registration_link,name="Resend_registration_link"),
    path('googleregistration/', GoogleAuthendication.as_view(), name='googleregistration'),
    path('guide_details/<int:id>/',GuideDetailView.as_view(),name="guide_details"), 
    path('forgotpassword/', Forgotpassword.as_view(), name='Forgotpassword'),
    path('reset_validate/<uidb64>/<token>/',views.resetpassword, name='reset_validate'),
    path('reset-password/<str:uidb64>/', ResetPassword.as_view()),
]
            