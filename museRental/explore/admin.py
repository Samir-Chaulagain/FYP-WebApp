from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Category)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'instrument_brand', 'category', 'user', 'is_published', 'is_sold')
    list_filter = ('category', 'user', 'is_published', 'is_sold')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'lessor':
            qs = qs.filter(user=request.user)
        return qs
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            # Limit the choices to users with the role 'lessor'
            kwargs['queryset'] = User.objects.filter(role='lessor')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Item, ItemAdmin)

admin.site.register(saved_item)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('item','user','Total_days')
    list_filter = ('item', 'user')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'customer':
            qs = qs.filter(user=request.user)
        return qs
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            # Limit the choices to users with the role 'lessor'
            kwargs['queryset'] = User.objects.filter(role='customer')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
admin.site.register(Customer,CustomerAdmin)