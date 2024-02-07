from django import template

from explore.models import saved_item

register = template.Library()


@register.simple_tag(name='is_item_already_saved')
def is_item_already_saved(item, user):
    applied = saved_item.objects.filter(item=item, user=user)
    if applied:
        return True
    else:
        return False
