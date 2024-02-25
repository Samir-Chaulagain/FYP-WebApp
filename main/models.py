from django.db import models
from datetime import datetime
# Create your models here.

# model for blog post
# image field addded 

class Post(models.Model):
    image = models.ImageField(upload_to='images/', default='default_image.jpg')
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=1000000)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    
    def __str__(self):
        return self.title



class Dispute(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    invoice = models.CharField(max_length=200)
    issue = models.TextField()

    def __str__(self):
        return self.invoice
