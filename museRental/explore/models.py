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

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    instrument_model = models.CharField(max_length=60,  default='Default model Name')
    instrument_brand = models.CharField(max_length=60, default='Default Brand Name')
    price = models.FloatField()
    is_sold = models.BooleanField(default=False)
    instrument_image1 = models.ImageField(upload_to='img/instrument_images/',default='img/inst1/')
    instrument_image2 = models.ImageField(upload_to='img/instrument_images/',default='img/inst1/')
    instrument_image3 = models.ImageField(upload_to='img/instrument_images/',default='img/inst1/')    
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Rentitem(models.Model):
    Rentitem_id = models.AutoField
    name = models.ForeignKey(Item, on_delete=models.CASCADE)

    Rentitem_Date_of_Booking = models.DateField(blank=True,null=True)
    Rentitem_Date_of_Return = models.DateField(blank=True,null=True)
    Total_days = models.IntegerField()
    Advance_amount = models.IntegerField(blank=True,null=True)
    Rentitem_Total_amount = models.IntegerField(blank=True,null=True)
    isAvailable = models.BooleanField(default=True)
    customer_email = models.CharField(max_length=100)
    request_responded_by = models.CharField(max_length=100,blank=True,null=True)
    request_status = models.CharField(max_length=30,default="Pending")

    def __str__(self):
        return self.customer_email + ": "


