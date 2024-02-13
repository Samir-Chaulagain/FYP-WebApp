import datetime
from django.db import models
from accounts.models import User
from ckeditor.fields import RichTextField
# Create your models here.
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
# User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
item_type = (
    ('1', "Solo"),
    ('2', "Package"),
    ('3', "Sound Accessories"),
)    
class Item(models.Model):
    
    name = models.CharField(max_length=255)
    instrument_brand = models.CharField(max_length=60, default='Default Brand Name')
    instrument_model = models.CharField(max_length=60,  default='Default model Name')
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    description = RichTextField()
    location = models.CharField(max_length=55,default='Thimi')
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField(default=1)
    item_type = models.CharField(choices=item_type, max_length=1,default=False)
    price = models.FloatField()
    is_published = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)   
    user = models.ForeignKey(User, related_name='User', on_delete=models.CASCADE,default=False)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    def get_item_type_display_name(self):
        # Use a dictionary to map item type numbers to their corresponding names
        item_type_mapping = dict(item_type)
        return item_type_mapping.get(self.item_type, 'Unknown') 
    
class Image(models.Model):
    item=models.ForeignKey(Item, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='images/')

    def __str__(self):
        return str(self.pk)    
    

class Customer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item= models.ForeignKey(Item, on_delete=models.CASCADE)
    Rentitem_Date_of_Booking = models.DateField(blank=True,null=True)
    Rentitem_Date_of_Return = models.DateField(blank=True,null=True)
    Total_days = models.IntegerField(default=0)
    Rentitem_Total_amount = models.IntegerField(blank=True,null=True)
    isAvailable = models.BooleanField(default=True)    
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    time= models.TimeField(default=datetime.time(hour=0, minute=0))
    
    request_status = models.CharField(max_length=30,default="Pending")
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)



    def __str__(self):
        return self.item.name
     
    
class saved_item(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)


    def __str__(self):
        return self.item.name
    
    
class applieditems(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)


    def __str__(self):
        return self.item.name
     
class Review(models.Model):
    item = models.ForeignKey(Item, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ]
    )
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"rating: {self.rating}, Comment: {self.comment}"



