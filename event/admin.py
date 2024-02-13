from django.contrib import admin
from event.models import *
from leaflet_point.admin import LeafletPointAdmin

admin.site.register(Event, LeafletPointAdmin)
# Register your models here.
admin.site.register(Category)



class BookingAdmin(admin.ModelAdmin):
    list_display = ('event','user','is_paid')
admin.site.register(Booking,BookingAdmin)
admin.site.register(saved_event)

