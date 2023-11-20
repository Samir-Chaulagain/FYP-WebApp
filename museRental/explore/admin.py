from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Customer)
admin.site.register(saved_item)
admin.site.register(Rentitem)