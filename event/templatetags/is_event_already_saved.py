from django import template

from event.models import saved_event

register = template.Library()


@register.simple_tag(name='is_event_already_saved')
def is_event_already_saved(event, user):
    applied = saved_event.objects.filter(event=event, user=user)
    if applied:
        return True
    else:
        return False
