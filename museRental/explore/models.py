from django.db import models
from accounts.models import User
from ckeditor.fields import RichTextField
# Create your models here.
from django.contrib.auth import get_user_model
# User = get_user_model()

item_type = (
    ('1', "Solo"),
    ('2', "Package"),
    ('3', "Others"),
)    
class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Item(models.Model):
    
    name = models.CharField(max_length=255)
    instrument_brand = models.CharField(max_length=60, default='Default Brand Name')
    instrument_model = models.CharField(max_length=60,  default='Default model Name')
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    description = RichTextField()
      
    item_type = models.CharField(choices=item_type, max_length=1,default=False)
    price = models.FloatField()
    is_published = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    # is_sold = models.BooleanField(default=False)

    instrument_image1 = models.ImageField(upload_to='images/',default='img/inst1/')
    instrument_image2 = models.ImageField(upload_to='images/',default='img/inst1/')
    instrument_image3 = models.ImageField(upload_to='images/',default='img/inst1/')    
    user = models.ForeignKey(User, related_name='User', on_delete=models.CASCADE,default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
    

class Customer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item= models.ForeignKey(Item, on_delete=models.CASCADE)
    Rentitem_Date_of_Booking = models.DateField(blank=True,null=True)
    Rentitem_Date_of_Return = models.DateField(blank=True,null=True)
    Total_days = models.IntegerField(default=0)
    Advance_amount = models.IntegerField(blank=True,null=True)
    Rentitem_Total_amount = models.IntegerField(blank=True,null=True)
    isAvailable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    request_status = models.CharField(max_length=30,default="Pending")


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
     
    




