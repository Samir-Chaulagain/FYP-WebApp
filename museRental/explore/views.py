from django.shortcuts import get_object_or_404, render,redirect
from .forms import add_item_form
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .models import Item
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from accounts.models import User
from explore.forms import *
from explore.models import *
from accounts.permission import *
from datetime import datetime



# Create your views here.

def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

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


# View instruments
def showdetails(request,pk):
    item = get_object_or_404(Item, pk=pk)
   

    return render(request, 'explore/details.html', {
        'item': item,
        
    })

def CheckAvailability(request,name):
    if('email' not in request.session):
        return redirect('/signin/')

    Rentinstrument_Date_of_Booking=request.POST.get('Rentinstrument_Date_of_Booking','')
    Rentinstrument_Date_of_Return=request.POST.get('Rentinstrument_Date_of_Return','')
    print(Rentinstrument_Date_of_Booking)
    Rentinstrument_Date_of_Booking = datetime.strptime(Rentinstrument_Date_of_Booking, '%Y-%m-%d').date()
    print(Rentinstrument_Date_of_Booking)
    Rentinstrument_Date_of_Return = datetime.strptime(Rentinstrument_Date_of_Return, '%Y-%m-%d').date()

    rentinstrument = Rentinstrument.objects.filter(name=name)
    Item = Item.objects.get(name=name)

    email = request.session.get('email')
    user = User.objects.get(email )

   

    if Rentinstrument_Date_of_Booking < date.today():
        Incorrect_dates = "Please give proper dates"
        return render(request,'Owner_showdetails.html',{'Incorrect_dates':Incorrect_dates,'Item':Item,'user':user})

    if Rentinstrument_Date_of_Return < Rentinstrument_Date_of_Booking:
        Incorrect_dates = "Please give proper dates"
        return render(request,'Owner_showdetails.html',{'Incorrect_dates':Incorrect_dates,'item':Item,'user':user})
    
    days=(Rentinstrument_Date_of_Return-Rentinstrument_Date_of_Booking).days+1
    total=days*Item.price
    
    rent_data = {"Rentinstrument_Date_of_Booking":Rentinstrument_Date_of_Booking, "Rentinstrument_Date_of_Return":Rentinstrument_Date_of_Return,"days":days, "total":total}
    
    for rv in rentinstrument:

        # if (Rentinstrument_Date_of_Booking < rv.Rentinstrument_Date_of_Booking and Rentinstrument_Date_of_Return < rv.Rentinstrument_Date_of_Booking) or (Rentinstrument_Date_of_Booking > rv.Rentinstrument_Date_of_Return and Rentinstrument_Date_of_Return > rv.Rentinstrument_Date_of_Return):
        #     Available = True
        #     return render(request,'Owner_showdetails.html',{'Available':Available,'instrument':instrument,'owner':owner,'rent_data':rent_data,'no_of_pending_request':no_of_pending_request})

        if (rv.Rentinstrument_Date_of_Booking >= Rentinstrument_Date_of_Booking and Rentinstrument_Date_of_Return >= rv.Rentinstrument_Date_of_Booking) or (Rentinstrument_Date_of_Booking >= rv.Rentinstrument_Date_of_Booking and Rentinstrument_Date_of_Return <= rv.Rentinstrument_Date_of_Return) or (Rentinstrument_Date_of_Booking <= rv.Rentinstrument_Date_of_Return and Rentinstrument_Date_of_Return >= rv.Rentinstrument_Date_of_Return):
            if rv.isAvailable:
                Available = True
                Message = "Note that somebody has also requested for this instrument from " + str(rv.Rentinstrument_Date_of_Booking) + " to " + str(rv.Rentinstrument_Date_of_Return)
                return render(request,'Owner_showdetails.html',{'Message':Message,'Available':Available,'instrument':instrument,'owner':owner,'rent_data':rent_data,'no_of_pending_request':no_of_pending_request})

            NotAvailable = True
            return render(request,'Owner_showdetails.html',{'NotAvailable':NotAvailable,'dates':rv,'instrument':instrument,'owner':owner,'no_of_pending_request':no_of_pending_request})
    
    Available = True
    return render(request,'Owner_showdetails.html',{'Available':Available,'instrument':instrument,'owner':owner,'rent_data':rent_data,'no_of_pending_request':no_of_pending_request})