# views.py
from rest_framework import viewsets
from .models import MainPlace, TripPlanning
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.http import JsonResponse
from django.core.mail import send_mail
from account.views import *
from django.conf import settings
from rest_framework.generics import RetrieveUpdateDestroyAPIView,CreateAPIView, ListCreateAPIView, UpdateAPIView


class MainPlaceViewSet(viewsets.ModelViewSet):
    queryset = MainPlace.objects.all()
    serializer_class = MainPlaceSerializer
    
class TripPlanningViewSet(viewsets.ModelViewSet):
    queryset = TripPlanning.objects.all()
    serializer_class = TripPlanningSerializer
    
    def create(self, request, *args, **kwargs):
        
        main_place_id = request.data.get('maintable_id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        if serializer:
            try:
                main_place = MainPlace.objects.get(pk=main_place_id)
                main_place.trip_planning.add(serializer.instance)
            except MainPlace.DoesNotExist:
                pass
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()  

        # Define which fields can be updated via PATCH
        allowed_fields = ['image','description','place','date']

        # Validate that the fields being updated are allowed
        for field, value in request.data.items():
            if field in allowed_fields:
                setattr(instance, field, value)
            else:
                return Response(
                    {'detail': f'Field {field} cannot be updated via PATCH'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    

class MainPlaceViewSetsingleView(generics.RetrieveAPIView):
    serializer_class = MainPlaceSerializer
    queryset = MainPlace.objects.all()
    lookup_field = 'id'


class MainPlaceGuideViewSet(generics.ListAPIView):
    serializer_class = MainPlaceSerializer
    lookup_field ='id '
    def get_queryset(self):
        return MainPlace.objects.filter(user__role='guide',is_show = True)



class UserTripPlansListView(generics.ListAPIView):
    serializer_class = MainPlaceSerializer
    lookup_field ='id'
    def get_queryset(self):
         user_id = self.kwargs['id'] 
         return MainPlace.objects.filter(user_id=user_id)



class Invitations(generics.GenericAPIView):
    serializer_class = Invite_Serializer

    def get(self, request, send_to):
        invitations = Invitation.objects.filter(send_to=send_to)
        serializer = self.serializer_class(invitations, many=True)
        return Response(serializer.data)

  
class InvitationUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InvitationUpdateSerializer
    queryset = Invitation.objects.all()
    lookup_field = 'id'


    def partial_update(self, request, *args, **kwargs):
        updated_status = request.data.get("updatedStatus")
        instance = self.get_object()
        if instance.status == request.data.get('status'):
            return Response({'message': 'Invitation is already updated.'}, status=status.HTTP_200_OK)
        instance.status = updated_status
        instance.save()
        return Response({"message": "Invitation updated successfully"})


class InviterInvitees(generics.ListAPIView):
    serializer_class = InvitationSerializer
    def get_queryset(self):
        email = self.kwargs['email']
        return Invitation.objects.filter(trip__user__email=email)
    



class InviteFriendView(APIView):
    def post(self, request):
        serializer = InviteFriendsSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            trip_id = request.data.get('trip_id') 
            
            # Create an Invitation instance
            try:
                trip = MainPlace.objects.get(pk=trip_id)
                invitation = Invitation(trip=trip, send_to=email)
                invitation.save()
            except MainPlace.DoesNotExist:
                return Response({"error": "Trip not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            link = f"http://localhost:5173/user/trip-page-invitee/{trip_id}"

            # Build the email message
            subject = "Invitation to a Trip Plan"
            message = (
                f"You're invited to join a trip plan on {settings.WEBSITE_NAME}.\n"
                f"Click the link below to access the trip plan:\n"
                f"{link}"
            )

            # Send the email
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,  # Use your sender email from Django settings
                [email],
                fail_silently=False,
            )

            return Response({"message": "Invitation sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

