import logging
import uuid

from django.db.models import Q
import json
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy

from event.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from event.forms import EventBooked, EventEditForm,EventSavedForm
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Create your views here.
def event(request):
    id = uuid.uuid4()
    print(id)
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    all_events = Event.objects.all()

    

    

    if category_id:
        filtered_events = all_events.filter(category__id=category_id)
    else:
        filtered_events = all_events

    if query:
        filtered_events = filtered_events.filter(Q(name__icontains=query) | Q(description__icontains=query))
    paginator = Paginator(filtered_events, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    print(f"Category ID: {category_id}, Filtered Events Count: {filtered_events.count()}")

    return render(request, 'events/event.html', {
        'page_obj': page_obj,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        'uuid': id,
        'events': filtered_events,
    })

def showdetails(request,pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event-details.html', {
        'event': event,})

# @login_required(login_url=reverse_lazy('accounts:login'))
# @login_required
# def book_event(request, pk):
#     event = get_object_or_404(Event, pk=pk)
#     form = BookingForm(request.POST)
#     if request.method == 'POST':
       
#         if form.is_valid():
           
#             num_tickets = form.cleaned_data['num_tickets']
#             total_price = num_tickets * event.ticket_price

#             # Create a booking record
#             booking = Booking.objects.create(
#                 event=event,
#                 user=request.user,
#                 num_tickets=num_tickets,
#                 total_price=total_price,
#             )


#             return render(request, 'events/booking_confirmation.html', {'booking': booking})
#         else:
#             form = BookingForm()

        

#     context = {'event': event, 'form': form}
#     return render(request, 'events/event-details.html', context)


@login_required(login_url=reverse_lazy('accounts:login'))
def event_saved_view(request, pk):
    form = EventSavedForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    saved_events = saved_event.objects.filter(user=request.user.id, event=pk)

    if not saved_events:
        if request.method == 'POST':
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(request, 'You have successfully saved this item!')
                return redirect(reverse("event:event-details", kwargs={'pk': pk}))

        else:
            return redirect(reverse("event:event-details", kwargs={'pk': pk}))

    
    return redirect(reverse("event:event-details", kwargs={'pk': pk}))

@login_required(login_url=reverse_lazy('accounts:login'))
def delete_savedevent_view(request, pk):
    try:
        event = saved_event.objects.filter(event=pk, user=request.user).first()

        # Debugging prints
        print(f"Requested pk: {pk}")
        print(f"Request user: {request.user}")
        print(f"Found saved event: {saved_event.event}")

        if event:
            event.delete()
            messages.success(request, 'Saved item was successfully deleted!')
        else:
            messages.error(request, 'Saved item not found or you do not have permission to delete it.')
    except saved_event.DoesNotExist:
        messages.error(request, 'Saved item not found or you do not have permission to delete it.')

    # Assuming 'event-details' is a valid URL pattern, redirect to it after deletion
    return redirect('event:event-details', pk=pk)

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@login_required(login_url=reverse_lazy('accounts:login'))
def mark_paid_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user.id)
    if booking:
        booking.is_paid = True
        booking.save()
    
    # Send email to the user
    subject = 'Payment Confirmation'
    html_message = render_to_string('events/booking_confirmation.html', {'booking': booking})
    plain_message = strip_tags(html_message)
    from_email = 'muserentalhub@gmail.com'
    to_email = request.user.email  # Assuming the user is associated with the event
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
    
    return redirect('explore:dashboard')



@login_required(login_url=reverse_lazy('accounts:login'))
def event_view(request, pk):
    # Assuming `pk` is the event pk.
    event = get_object_or_404(Event, pk=pk)
    user = get_object_or_404(User, id=request.user.id)

    if request.method == 'POST':
        num_tickets = int(request.POST.get('no_of_tickets', 0))

        # Check if the user has already booked tickets for this event
        events = Booking.objects.filter(user=user, event=event).first()
        total_price = num_tickets * event.ticket_price

        if num_tickets > 0:
            if not events:
                instance = Booking(
                    user=user,
                    event=event,
                    num_tickets=num_tickets,
                    total_price=total_price,
                    
                )
                instance.save()

                messages.success(request, 'You have successfully applied for this event!')
                return redirect(reverse("event:event-details", kwargs={'pk': pk}))
            else:
                messages.error(request, 'You have already booked tickets for this event!')
        else:
            messages.error(request, 'Please enter a valid number of tickets (greater than zero).')

    return render(request, 'events/event-details.html', {'event': event})









   
