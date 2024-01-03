from datetime import datetime
from django.db import models
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
    description = models.TextField()
    date = models.DateTimeField(default=datetime.now)
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)    
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status_choice = (
       
        ('active', 'Active'),
        ('deleted', 'Deleted'),
        ('time out', 'Time Out'),
        ('completed', 'Completed'),
        ('cancel', 'Cancel'),
    )
    status = models.CharField(choices=status_choice, max_length=10)
    maximum_attende = models.PositiveIntegerField()
    created_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booked_events')
    num_tickets = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # Add other booking-related fields if needed, e.g., payment_status, booking_date, etc.
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
def __str__(self):
        return f"{self.user.username} booked {self.num_tickets} tickets for {self.event.name}"



class saved_event(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)


    def __str__(self):
        return self.event.name
