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
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    instrument_model = models.CharField(max_length=60)
    instrument_brand = models.CharField(max_length=60)
    price = models.FloatField()
    instrument_image1 = models.ImageField(upload_to='img/instrument_images/')
    instrument_image2 = models.ImageField(upload_to='img/instrument_images/')
    instrument_image3 = models.ImageField(upload_to='img/instrument_images/')


    
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name




