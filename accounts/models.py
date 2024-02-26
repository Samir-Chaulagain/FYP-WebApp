from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from accounts.managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
Gender_TYPE = (
    ('M', _("Male")),
    ('F', _("Female")),
)

ROLE = (
    ('customer', _("customer")),
    ('lessor', _("lessor")),
)
DOCUMENT_TYPES = (
        ('Citizenship', _('Citizenship')),
        ('License', _('License')),
        ('Passport', _('Passport')),
        ('Others', _('Others')),
    )

class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        blank=False,
        
    )

    
    role = models.CharField(choices=ROLE, max_length=10)
    gender = models.CharField(choices=Gender_TYPE, max_length=15)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    photo=models.ImageField(upload_to='images',null=True, blank=True, default='images/default_image.png')
    is_verified=models.BooleanField(default=False)
    
    document_type = models.CharField(choices=DOCUMENT_TYPES, max_length=20,default='citizenship')
    document_photo=models.ImageField(upload_to='images',null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    objects = CustomUserManager()

