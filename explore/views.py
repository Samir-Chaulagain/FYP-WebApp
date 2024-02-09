
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.template.loader import render_to_string

from .forms import *
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .models import Item
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from accounts.models import User
from explore.forms import *
from explore.models import *
from event.models import saved_event,Booking
from accounts.permission import *
import json

import logging
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


from datetime import date, datetime
User = get_user_model()


# Create your views here.

#items function to display/render explore page 
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Item, Category

def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    item_type = request.GET.get('item_type', '')  # Get the item type from the query parameters

    categories = Category.objects.all()
    item_list = Item.objects.filter(is_published=True, is_sold=False).order_by('-created_at')

    # Apply category filter
    if category_id:
        item_list = item_list.filter(category_id=category_id)

    # Apply query filter
    if query:
        item_list = item_list.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Apply item type filter
    if item_type:
        item_list = item_list.filter(item_type=item_type)

    paginator = Paginator(item_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'explore/explore.html', {
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        'page_obj': page_obj,
        'items': page_obj,  # Pass paginated items instead of the whole item_list
    })


# View instrument details
def showdetails(request,id):
    item = get_object_or_404(Item, id=id)
    reviews = Review.objects.filter(item=item) 
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    return render(request, 'explore/details.html', {
        'item': item,'reviews': reviews,'average_rating': average_rating})



@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_customer
def rate_item(request, id):
    if request.method == 'POST':
        val = request.POST.get('val')
        comment = request.POST.get('comment')
        item = get_object_or_404(Item, id=id)
        user = request.user

        if not val:  # Check if val is empty
            return JsonResponse({'success': False, 'error': 'Rating value is missing'}, status=400)

        rating = int(val)

        # Check if the user has already rated the item
        try:
            rating_review = Review.objects.get(item=item, user=user)
            rating_review.rating = rating
            rating_review.comment = comment
            rating_review.save()
        except Review.DoesNotExist:
            # Create a new rating if the user has not rated the item yet
            rating_review = Review.objects.create(item=item, user=user, rating=rating, comment=comment)

        # Redirect the user to the details page of the item
        return redirect('explore:details', id=item.id)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_lessor
def add_item(request):
    # Provide the ability to create item post
    form = additemForm(request.POST or None, request.FILES or None)

    user = get_object_or_404(User, id=request.user.id)
    categories = Category.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            item = form.save(commit=False)
            item.latitude = request.POST.get('latitude')
            item.longitude = request.POST.get('longitude')
            item.save()


            # Save tags
            form.save_m2m()
            # Loop through each uploaded file and associate it with the created item
            for file in request.FILES.getlist('file'):
                # Create an Image instance and associate it with the created item
                Image.objects.create(item=instance, image=file)
            

            messages.success(
                request, 'You have successfully posted your item! Please wait for review.')
            
            
    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'explore/add-instrument.html', context)


@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_lessor
def item_edit_view(request, id=id):
    """
    Handle item Update

    """

    item = get_object_or_404(Item, id=id, user=request.user.id)
    categories = Category.objects.all()
    form = edititemForm(request.POST or None, instance=item)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # for save tags
        # form.save_m2m()
        messages.success(request, 'Your item Post Was Successfully Updated!')
        return redirect(reverse("explore:items", kwargs={
            'id': instance.id
        }))
    context = {

        'form': form,
        'categories': categories
    }

    return render(request, 'explore/item-edit.html', context)


# def search_result_view(request):
#     """
#         User can search item with multiple fields

#     """

#     item = item.objects.order_by('-timestamp')

#     # Keywords
#     if 'item_name_or_created_by' in request.GET:
#         item_name_or_created_by = request.GET['item_name_or_created_by']

#         if item_name_or_created_by:
#             item = item.filter(title__icontains=item_name_or_created_by) | item.filter(
#                 company_name__icontains=item_name_or_created_by)

    # location
    # item Type
    # if 'item_type' in request.GET:
    #     item_type = request.GET['item_type']
    #     if item_type:
    #         item = item.filter(item_type__iexact=item_type)

    # return render(request, 'explore/result.html', item)






@login_required(login_url=reverse_lazy('accounts:login'))
def dashboard(request):
        
    items = []
    saveditems = []
    savedevent = []
    applieditems = []
    appliedevent = []
    total_Customers = {}
    if request.user.role == 'lessor':
        items = Item.objects.filter(user=request.user.id)
    for item in items:
        count = Customer.objects.filter(item=item.id).count()
        total_Customers[item.id] = count
    if request.user.role == 'customer':
        saveditems = saved_item.objects.filter(user=request.user.id)
        applieditems = Customer.objects.filter(user=request.user.id)
        savedevent=saved_event.objects.filter(user=request.user.id)
        appliedevent=Booking.objects.filter(user=request.user.id)

    if request.user.role == 'lessor':
        savedevent=saved_event.objects.filter(user=request.user.id)
        appliedevent=Booking.objects.filter(user=request.user.id)
    
    context = {
     'items': items,
        'saveditems': saveditems,
        'applieditems':applieditems,
        'total_Customers': total_Customers,
        'savedevent': savedevent,
        'appliedevent': appliedevent,
        
    }
    return render(request, 'explore/dashboard.html', context)


@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_lessor
def all_Customers_view(request, id):

    all_Customers = Customer.objects.filter(item=id)

    context = {

        'all_Customers': all_Customers
    }

    return render(request, 'explore/all-customers.html', context)

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_lessor
def Customer_details_view(request, id):

    Customer = get_object_or_404(User, id=id)

    context = {

        'Customer': Customer
    }

    return render(request, 'explore/customer-details.html', context)

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_lessor
def delete_item(request, id):

    item = get_object_or_404(Item, id=id, user=request.user.id)

    if item:

        item.delete()
        messages.success(request, 'Your item Post was successfully deleted!')

    return redirect('explore:dashboard')


#  for mmarking sold 
# @login_required(login_url=reverse_lazy('accounts:login'))
# @user_is_lessor
# def make_complete_item_view(request, id):
#     item = get_object_or_404(Item, id=id, user=request.user.id)

#     if item:
#         try:
#             item.is_sold = True
#             item.save()
#             messages.success(request, 'Your item was marked closed!')
#         except:
#             messages.success(request, 'Something went wrong !')
            
#     return redirect('explore:dashboard')

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_customer
def item_saved_view(request, id):
    form = ItemSavedForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    Customer = saved_item.objects.filter(user=request.user.id, item=id)

    if not Customer:
        if request.method == 'POST':
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(request, 'You have successfully saved this item!')
                return redirect(reverse("explore:details", kwargs={'id': id}))

        else:
            return redirect(reverse("explore:details", kwargs={'id': id}))

    else:
        messages.error(request, 'You already saved this item!')
        return redirect(reverse("explore:details", kwargs={'id': id}))

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_customer
def delete_save_view(request, id):

    item = get_object_or_404(saved_item, id=id, user=request.user.id)

    if item:
        item.delete()
        messages.success(request, 'Saved item was successfully deleted!')

    return redirect('explore:dashboard')


from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from datetime import datetime, date
from .models import Customer, Item
from django.contrib.auth.decorators import login_required
# from .decorators import user_is_customer

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_customer
def CheckAvailability(request, id):
    customer = Customer.objects.filter(user=request.user.id, item_id=id)
    
    Rentitem_Date_of_Booking = request.POST.get('Rentitem_Date_of_Booking', '')
    Rentitem_Date_of_Return = request.POST.get('Rentitem_Date_of_Return', '')
    
    Rentitem_Date_of_Booking = datetime.strptime(Rentitem_Date_of_Booking, '%Y-%m-%d').date()
    Rentitem_Date_of_Return = datetime.strptime(Rentitem_Date_of_Return, '%Y-%m-%d').date()

    item = Item.objects.get(id=id)

    if Rentitem_Date_of_Booking < date.today():
        Incorrect_dates = "Please give proper dates"
        return render(request, 'explore/details.html', {'Incorrect_dates': Incorrect_dates, 'item': item})

    if Rentitem_Date_of_Return < Rentitem_Date_of_Booking:
        Incorrect_dates = "Please give proper dates"
        return render(request, 'explore/details.html', {'Incorrect_dates': Incorrect_dates, 'item': item})
    
    rentItem = Customer.objects.filter(item_id=id, isAvailable=True)
    
    for i in rentItem:
        if (i.Rentitem_Date_of_Booking <= Rentitem_Date_of_Return and Rentitem_Date_of_Booking <= i.Rentitem_Date_of_Return) and (Rentitem_Date_of_Booking <= i.Rentitem_Date_of_Return and Rentitem_Date_of_Return <= i.Rentitem_Date_of_Return):
            # Overlapping date range with an available item
            NotAvailable = True
            Message = "Note that somebody has also requested for this item from " + str(i.Rentitem_Date_of_Booking) + " to " + str(i.Rentitem_Date_of_Return)+" So there are some chances that you might not get it. As items are rented on First come first serve policy."
            messages.error(request, Message)
            # rent_data = {"Rentitem_Date_of_Booking": Rentitem_Date_of_Booking, "Rentitem_Date_of_Return": Rentitem_Date_of_Return, "days": (Rentitem_Date_of_Return - Rentitem_Date_of_Booking).days + 1, "total": item.price * ((Rentitem_Date_of_Return - Rentitem_Date_of_Booking).days + 1)}
            return render(request, 'explore/details.html', {'Message': Message, 'NotAvailable': NotAvailable, 'item': item, 'customer': customer})
    
    # No overlapping date ranges found, the item is available
    Available = True
    Message = "Items available to book for the given date range"

    rent_data = {"Rentitem_Date_of_Booking": Rentitem_Date_of_Booking, "Rentitem_Date_of_Return": Rentitem_Date_of_Return, "days": (Rentitem_Date_of_Return - Rentitem_Date_of_Booking).days + 1, "total": item.price * ((Rentitem_Date_of_Return - Rentitem_Date_of_Booking).days + 1)}
    return render(request, 'explore/details.html', {'Message': Message,'Available': Available, 'item': item, 'customer': customer, 'rent_data': rent_data})




@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_customer
def rent_item_view(request, id):
    user = get_object_or_404(User, id=request.user.id)
    Customers = Customer.objects.filter(user=user, item=id)
    
    if not Customers:
        if request.method == 'POST':
            Rentitem_Date_of_Booking = request.POST.get('Rentitem_Date_of_Booking', '')
            Rentitem_Date_of_Return = request.POST.get('Rentitem_Date_of_Return', '')
            latitude = request.POST.get('latitude','')
            longitude = request.POST.get('longitude','')

            Rentitem_Date_of_Booking = datetime.strptime(Rentitem_Date_of_Booking, '%b. %d, %Y').date()
            Rentitem_Date_of_Return = datetime.strptime(Rentitem_Date_of_Return, '%b. %d, %Y').date()

            item = get_object_or_404(Item, id=id)
            total_days = (Rentitem_Date_of_Return - Rentitem_Date_of_Booking).days + 1
            total_amount = total_days * item.price

            instance = Customer(
                user=user,
                item=item,
                Rentitem_Date_of_Booking=Rentitem_Date_of_Booking,
                Rentitem_Date_of_Return=Rentitem_Date_of_Return,
                Total_days=total_days,
                Rentitem_Total_amount=total_amount,
                latitude=latitude,
                longitude=longitude
                
                
            )
            instance.save()
            

            messages.success(request, 'You have successfully applied for this item!')
            return redirect(reverse("explore:details", kwargs={'id': id}))

    else:
        messages.error(request, 'You already applied for the item!')

    return redirect(reverse("explore:details", kwargs={'id': id}))
    




# Get or create a logger for this module
logger = logging.getLogger(__name__)

# Decorators to exempt CSRF protection and require POST method for this view
@csrf_exempt
@require_POST
def send_email_after_payment(request):
    
    try:
        
        data = json.loads(request.body)
        lessor_email = data.get('lessor_email')
        customer_email = data.get('customer_email')

        subject = 'Payment Successful'
        from_email = 'muserentalhub@gmail.com'

        # Load HTML templates and render with context
        lessor_html_message = render_to_string('explore/lessor_email_after_payment.html')
        customer_html_message = render_to_string('explore/customer_email_after_payment.html')

         # Send email to the lessor with lessor_html_message
        send_mail(subject, '', from_email, [lessor_email], html_message=lessor_html_message)
        print(lessor_email)

        # Send email to the customer with customer_html_message
        send_mail(subject, '', from_email, [customer_email], html_message=customer_html_message)
        print(customer_email)
        return JsonResponse({'status': 'success'})
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return JsonResponse({'status': 'error'}, status=500)









from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Customer

@require_POST
@csrf_exempt  # CSRF exemption for simplicity; consider using a decorator like csrf_protect in production
def update_status(request):
    user_id = request.POST.get('user_id')
    new_status = request.POST.get('new_status')
    print(new_status)
    
    customer = Customer.objects.get(id=user_id)
    customer.request_status = new_status
    customer.save()
    print("hello")
    return JsonResponse({'status': 'success'})
    



