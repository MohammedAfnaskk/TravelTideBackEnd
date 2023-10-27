# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'main-place', MainPlaceViewSet)
router.register(r'trip-planning', TripPlanningViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('MainPlaceViewSetsingleView/<int:id>/',MainPlaceViewSetsingleView.as_view(),name="MainPlaceViewSetsingleView"),
    path('guide-trip-plans/',MainPlaceGuideViewSet.as_view(),name="guide-trip-plans"),
    path('user_trip_plans/<int:id>/', UserTripPlansListView.as_view(), name='user_trip_plans-list'),
    path('users_invitations/<str:send_to>/', Invitations.as_view(), name='user-invitation-detail'),
    path('users_invitation/<int:id>/', InvitationUpdateView.as_view(), name='update-invitation'),
    path('invite-friends/', InviteFriendView.as_view(), name='invite-friends'),
    path('manage-tripmates/<str:email>', InviterInvitees.as_view(), name='inviter-invitees-list'),


]

