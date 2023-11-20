from django import template
register = template.Library()


@register.simple_tag(name='get_total_customer')
def get_total_customer(total_customers , item):

    return total_customers[item.id]
  
     



        

