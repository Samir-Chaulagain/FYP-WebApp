from django.shortcuts import get_object_or_404, render
from event.models import *
from django.contrib.auth.decorators import login_required
from event.forms import BookingForm


# Create your views here.
def event(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    event = Event.objects.all()

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

def showdetails(request,pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event-details.html', {
        'event': event,
        
    })

# @login_required(login_url=reverse_lazy('accounts:login'))
@login_required
def book_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = BookingForm(request.POST)
    if request.method == 'POST':
       
        if form.is_valid():
           
            num_tickets = form.cleaned_data['num_tickets']
            total_price = num_tickets * event.ticket_price

            # Create a booking record
            booking = Booking.objects.create(
                event=event,
                user=request.user,
                num_tickets=num_tickets,
                total_price=total_price,
            )


            return render(request, 'events/booking_confirmation.html', {'booking': booking})
        else:
            form = BookingForm()

        

    context = {'event': event, 'form': form}
    return render(request, 'events/event-details.html', context)


def paypal(request, pk):
    orders = Booking.objects.get(pk=pk)
    order = Booking.objects.all()

    return render(request, 'paypal.html', {'orders': orders, 'order': order})