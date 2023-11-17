from django.shortcuts import render
from event.models import *


# Create your views here.
def event(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    event = Event.objects.filter()

    if category_id:
        event = event.filter(category_id=category_id)

    if query:
        event = event.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'events/event.html', {
        'event': event,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

   
