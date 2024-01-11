from email.message import EmailMessage
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.template.loader import render_to_string
from .forms import *
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .models import Item
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from accounts.models import User
from explore.forms import *
from explore.models import *
from event.models import saved_event,Booking
from accounts.permission import *

from datetime import date, datetime
User = get_user_model()


# Create your views here.

#items function to display/render explore page 
def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_published=True).order_by('-created_at')

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'explore/explore.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

# View instrument details
def showdetails(request,id):
    item = get_object_or_404(Item, id=id)
   

    return render(request, 'explore/details.html', {
        'item': item})

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_lessor
def add_item(request):
    """
    Provide the ability to create item post
    """
    form = additemForm(request.POST or None, request.FILES or None)

    user = get_object_or_404(User, id=request.user.id)
    categories = Category.objects.all()

    if request.method == 'POST':

        if form.is_valid():

            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(
                    request, 'You have successfully posted your item! Please wait for review.')
            return redirect(reverse("explore:details", kwargs={
                                    'id': instance.id
                                    }))

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


# for mmarking sold 
@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_lessor
def make_complete_item_view(request, id):
    item = get_object_or_404(Item, id=id, user=request.user.id)

    if item:
        try:
            item.is_sold = True
            item.save()
            messages.success(request, 'Your item was marked closed!')
        except:
            messages.success(request, 'Something went wrong !')
            
    return redirect('explore:dashboard')

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

# for checking availability
@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_customer
def CheckAvailability(request, id):
    # user = get_object_or_404(User, id=request.user.id)
    customer = Customer.objects.filter(user=request.user.id, item_id=id)
    
    Rentitem_Date_of_Booking = request.POST.get('Rentitem_Date_of_Booking', '')
    Rentitem_Date_of_Return = request.POST.get('Rentitem_Date_of_Return', '')
    Rentitem_Date_of_Booking = datetime.strptime(Rentitem_Date_of_Booking, '%Y-%m-%d').date()
    Rentitem_Date_of_Return = datetime.strptime(Rentitem_Date_of_Return, '%Y-%m-%d').date()

    rentItem = Customer.objects.filter(user=request.user.id, item_id=id)
    item = Item.objects.get(id=id)

    if Rentitem_Date_of_Booking < date.today():
        Incorrect_dates = "Please give proper dates"
        return render(request, 'explore/details.html', {'Incorrect_dates': Incorrect_dates, 'item': item})

    if Rentitem_Date_of_Return < Rentitem_Date_of_Booking:
        Incorrect_dates = "Please give proper dates"
        return render(request, 'explore/details.html', {'Incorrect_dates': Incorrect_dates, 'item': item})
    
    days = (Rentitem_Date_of_Return - Rentitem_Date_of_Booking).days + 1
    total = days * item.price
    rent_data = {"Rentitem_Date_of_Booking": Rentitem_Date_of_Booking, "Rentitem_Date_of_Return": Rentitem_Date_of_Return, "days": days, "total": total}

    for i in rentItem:
        if (i.Rentitem_Date_of_Booking >= Rentitem_Date_of_Booking and Rentitem_Date_of_Return >= i.Rentitem_Date_of_Booking) or (Rentitem_Date_of_Booking >= i.Rentitem_Date_of_Booking and Rentitem_Date_of_Return <= i.Rentitem_Date_of_Return) or (Rentitem_Date_of_Booking <= i.Rentitem_Date_of_Return and Rentitem_Date_of_Return >= i.Rentitem_Date_of_Return):
            if i.isAvailable:
                Available = True
                Message = "Note that somebody has also requested for this item from " + str(i.Rentitem_Date_of_Booking) + " to " + str(i.Rentitem_Date_of_Return)
                return render(request, 'explore:check-availability', {'Message': Message, 'Available': Available, 'item': item, 'customer': customer, 'rent_data': rent_data})

            NotAvailable = True
            return render(request, 'explore/details.html', {'NotAvailable': NotAvailable, 'dates': i, 'item': item, 'customer': customer})

    Available = True
    return render(request, 'explore/details.html', {'Available': Available, 'item': item, 'customer': customer, 'rent_data': rent_data})


@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_customer
def rent_item_view(request, id):
    user = get_object_or_404(User, id=request.user.id)
    Customers = Customer.objects.filter(user=user, item=id)

    if not Customers:
        if request.method == 'POST':
            Rentitem_Date_of_Booking = request.POST.get('Rentitem_Date_of_Booking', '')
            Rentitem_Date_of_Return = request.POST.get('Rentitem_Date_of_Return', '')

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
                Rentitem_Total_amount=total_amount
            )
            instance.save()

            messages.success(request, 'You have successfully applied for this item!')
            return redirect(reverse("explore:details", kwargs={'id': id}))

    else:
        messages.error(request, 'You already applied for the item!')

    return redirect(reverse("explore:details", kwargs={'id': id}))
    

def paypal(request, id):
    orders = Customer.objects.get(id=id)
    order = Customer.objects.all()
    return render(request, 'paypal.html', {'orders': orders, 'order': order})