from django import template

from explore.models import Customer

register = template.Library()


@register.simple_tag(name='is_item_already_rented')
def is_item_already_rented(item, user):
    rented = Customer.objects.filter(item=item, user=user)
    if rented:
        return True
    else:
        return False
