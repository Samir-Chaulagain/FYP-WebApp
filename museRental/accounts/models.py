from django.db import models
from django.utils.translation import gettext as _
from accounts.managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
gender = (
    ('M', _("Male")),
    ('F', _("Female")),
)

ROLE = (
    ('customer', _("customer")),
    ('lessor', _("lessor")),
)

class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        blank=False,
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    role = models.CharField(choices=ROLE, max_length=10)
    gender = models.CharField(choices=gender, max_length=1)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    objects = CustomUserManager()