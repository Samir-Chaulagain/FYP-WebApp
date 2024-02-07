from django.contrib import admin
from event.models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Event)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('event','user','is_paid')
admin.site.register(Booking,BookingAdmin)
admin.site.register(saved_event)

