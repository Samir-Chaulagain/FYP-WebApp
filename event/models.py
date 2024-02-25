from datetime import datetime
from django.utils import timezone


from django.db import models
from ckeditor.fields import RichTextField
from accounts.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', default='default_image.jpg')
    description = RichTextField()
    date = models.DateTimeField(default=datetime.now)
    location = models.CharField(max_length=300,default="Default")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    category = models.ForeignKey(Category, related_name='events', on_delete=models.CASCADE)    
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_unavailable = models.BooleanField(default=False)  # New field added
    is_active = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)
    
    maximum_attende = models.PositiveIntegerField()
    created_date = models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Check if the event date has passed
        if self.date < timezone.now() or self.maximum_attende ==0:
                       
            self.is_unavailable = True  # Set is_available to False if the event date has passed
            
         
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name

            
class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booked_events')
    num_tickets = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    invoice_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    booked_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def save(self, *args, **kwargs):
        # Set is_paid to True when saving the booking after a successful payment
        if self.is_paid:
            # Decrease the number of attendees for the related event
            self.event.maximum_attende -= self.num_tickets

            # If the maximum_attende reaches 0, update the status of the event
            if self.event.maximum_attende == 0:
                self.event.is_active = False
                self.event.is_sold = True

            self.event.save()

        super().save(*args, **kwargs)

   

class saved_event(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)


    def __str__(self):
        return self.event.name
