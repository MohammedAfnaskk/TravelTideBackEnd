from django.db import models
from account.models import CustomUser


class TripPlanning(models.Model):
    image = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField( null=True, blank=True)
    
 

class MainPlace(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    main_place = models.CharField(max_length=20, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True) 
    place_image = models.ImageField(null=True,blank=True)
    note = models.TextField(null=True, blank=True)
    budget = models.IntegerField(null=True, blank=True)
    trip_planning=models.ManyToManyField(TripPlanning)
    is_show = models.BooleanField(default=True, null=True, blank=True)

    STATUS_CHOICES = [
        ('In Progress', 'In Progress'), 
        ('Completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True)



class Invitation(models.Model):
    trip = models.ForeignKey(MainPlace, on_delete=models.CASCADE)  
    send_to = models.EmailField()
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=(("accepted","Accepted"),("pending","Pending"),("rejected","Rejected")), default="pending")