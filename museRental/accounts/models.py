# from django.db import models

# # Create your models here.

# class Customer(models.Model):
#     customer_id = models.AutoField
#     customer_firstname = models.CharField(max_length=60)
#     customer_lastname = models.CharField(max_length=60)
#     customer_address = models.CharField(max_length=600)
#     customer_email = models.CharField(max_length=100)
#     customer_password = models.CharField(max_length=32)
#     customer_dob = models.DateField()
#     customer_mobileno = models.CharField(max_length=10)
#     customer_gender = models.CharField(max_length=15)
#     customer_citizenship = models.ImageField(upload_to='img/Customer_citizen/')
#     customer_city = models.CharField(max_length=30)
#     customer_state = models.CharField(max_length=30)
#     customer_country = models.CharField(max_length=30)
#     customer_pincode = models.IntegerField()

#     def __str__(self):
#         return self.customer_email + ": " + str(self.customer_license)


from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext as _
from accounts.managers import CustomUserManager

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
    pdf_document = models.FileField(upload_to='pdf_documents/')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # Add related_name attributes to resolve the conflicts
    groups = models.ManyToManyField(Group, verbose_name=_("groups"), blank=True, help_text=_("The groups this user belongs to. A user will get all permissions granted to each of their groups."), related_name="user_accounts_groups")
    user_permissions = models.ManyToManyField(Permission, verbose_name=_("user permissions"), blank=True, help_text=_("Specific permissions for this user."), related_name="user_accounts_permissions")

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    objects = CustomUserManager()