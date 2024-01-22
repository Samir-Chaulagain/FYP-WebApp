from django import template

from event.models import Booking

register = template.Library()


@register.simple_tag(name='is_event_already_booked')
def is_event_already_booked(event, user):
    rented = Booking.objects.filter(event=event, user=user)
    if rented:
        return True
    else:
        return False
