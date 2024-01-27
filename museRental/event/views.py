import logging
import uuid
import requests
import json
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
import requests
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
    event = Event.objects.all()

    paginator = Paginator(event, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if category_id:
        event = event.filter(category_id=category_id)

    if query:
        event = event.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'events/event.html', {
        'page_obj': page_obj,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        'uuid':id
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

    else:
        messages.error(request, 'You already saved this item!')
    return redirect(reverse("event:event-details", kwargs={'pk': pk}))

@login_required(login_url=reverse_lazy('accounts:login'))
def delete_savedevent_view(request, pk):

    event = get_object_or_404(saved_event, pk=pk, user=request.user.pk)

    if event:
        event.delete()
        messages.success(request, 'Saved item was successfully deleted!')

    return redirect('explore:dashboard')




@login_required(login_url=reverse_lazy('accounts:login'))
def mark_paid_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user.id)
    if booking:
        booking.is_paid = True
        booking.save()
    
    return redirect('explore:dashboard')



@login_required(login_url=reverse_lazy('accounts:login'))
def event_view(request, pk):
    # Assuming `pk` is the event pk.
    event = get_object_or_404(Event, pk=pk)
    user = get_object_or_404(User, id=request.user.id)
    form = EventBooked(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            num_tickets = form.cleaned_data['num_tickets']

            # Check if the user has already booked tickets for this event
            events = Booking.objects.filter(user=user, event=event).first()
            total_price = num_tickets * event.ticket_price
            if not events:
                instance = Booking(
                    user=user,
                    event=event,
                    num_tickets=num_tickets,
                    total_price=total_price,
                    # Add other fields if needed
                )
                instance.save()

                messages.success(request, 'You have successfully applied for this event!')
                return redirect(reverse("event:event-details", kwargs={'pk': pk}))
            else:
                messages.error(request, 'You have already booked tickets for this event!')
        else:
            messages.error(request, 'Invalid form submission. Please check the form data.')

    return render(request, 'events/event-details.html', {'form': form, 'event': event})


logger = logging.getLogger(__name__)
@csrf_exempt
@require_POST
def send_email_after_payment(request):
    try:
        data = json.loads(request.body)
        receiver_email = data.get('receiver_email')

        subject = 'Payment Successful'
        message = 'User request for Your Event.Payment was successful.User loaction is'
        from_email = 'muserentalhub@gmail.com'
        recipient_list = [receiver_email]
        print("Hello", recipient_list)

        send_mail(subject, message, from_email, recipient_list)

        return JsonResponse({'status': 'success'})
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return JsonResponse({'status': 'error'}, status=500)



from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Event, Booking
from .forms import EventEditForm
import requests
import json

def payment(request, id):
    user = get_object_or_404(User, id=request.user.id)
    event = get_object_or_404(Event, id=id)
    
    form = EventEditForm(request.POST or None)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        payment_token = data.get('payment_token')
        payment_amount = data.get('payment_amount')
        print(payment_token)
        khalti_secret_key = "test_secret_key_ce1adf77ac904ffbba3bc3687d287103"
        verification_url = "https://khalti.com/api/v2/payment/verify/"
        headers = {
            'Authorization': f'key {khalti_secret_key}',
        }
        payload = {
            'token': payment_token,
            'amount': payment_amount,
        }

        response = requests.post(verification_url, headers=headers, json=payload)

        if response.status_code == 200:
            # Payment verification successful
            if form.is_valid():
                num_tickets = form.cleaned_data['num_tickets']
                total_price = num_tickets * event.ticket_price

                # Check if the user has already booked tickets for this event
                booking, created = Booking.objects.get_or_create(user=user, event=event)

                if not created:
                    booking.num_tickets = num_tickets
                    booking.total_price = total_price
                    booking.save()

                    messages.success(request, 'Booking updated successfully!')
                    return JsonResponse({'success': True})
                else:
                    booking.num_tickets = num_tickets
                    booking.total_price = total_price
                    booking.is_paid = True
                    booking.save()

                    messages.success(request, 'Booking created successfully!')
                    return JsonResponse({'success': True})
            else:
                messages.error(request, 'Invalid form submission. Please check the form data.')
                return JsonResponse({'success': False, 'error': 'Invalid form submission.'})
        else:
            # Payment verification failed
            messages.error(request, 'Payment verification failed. Please try again.')
            return JsonResponse({'success': False, 'error': 'Payment verification failed.'})

    return render(request, 'explore/dashboard.html', {'form': form, 'event': event})




   
