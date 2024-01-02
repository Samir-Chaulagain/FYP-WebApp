from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Category)
admin.site.register(Item)
admin.site.register(saved_item)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('item','user')
    
admin.site.register(Customer,CustomerAdmin)