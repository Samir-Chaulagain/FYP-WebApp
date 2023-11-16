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
    return render(request, 'explore/explore.html')


# View instruments

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_lessor


def upload_items(request):   
    form = add_item_form(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    categories = Category.objects.all()
    if form.is_valid():

            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(
                    request, 'Successfully posted Instrument.')
            return redirect(reverse("exlore:items", kwargs={
                                    'id': instance.id
                                    }))

    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'explore/add-instrument.html',context)



# rent instrument
def CheckAvailability(request,instrument_license_plate):
    if('user_email' not in request.session):
        return redirect('/signin/')

    Rentinstrument_Date_of_Booking=request.POST.get('Rentinstrument_Date_of_Booking','')
    Rentinstrument_Date_of_Return=request.POST.get('Rentinstrument_Date_of_Return','')
    print(Rentinstrument_Date_of_Booking)
    Rentinstrument_Date_of_Booking = datetime.strptime(Rentinstrument_Date_of_Booking, '%Y-%m-%d').date()
    print(Rentinstrument_Date_of_Booking)
    Rentinstrument_Date_of_Return = datetime.strptime(Rentinstrument_Date_of_Return, '%Y-%m-%d').date()

    rentinstrument = Rentinstrument.objects.filter(instrument_license_plate=instrument_license_plate)
    instrument = instrument.objects.get(instrument_license_plate=instrument_license_plate)

    owner_email = request.session.get('user_email')
    owner = User.objects.get(Owner_email=owner_email)

    no_of_pending_request=count_pending_rent_request()

    if Rentinstrument_Date_of_Booking < date.today():
        Incorrect_dates = "Please give proper dates"
        return render(request,'Owner_showdetails.html',{'Incorrect_dates':Incorrect_dates,'instrument':instrument,'owner':owner,'no_of_pending_request':no_of_pending_request})

    if Rentinstrument_Date_of_Return < Rentinstrument_Date_of_Booking:
        Incorrect_dates = "Please give proper dates"
        return render(request,'Owner_showdetails.html',{'Incorrect_dates':Incorrect_dates,'instrument':instrument,'owner':owner,'no_of_pending_request':no_of_pending_request})
    
    days=(Rentinstrument_Date_of_Return-Rentinstrument_Date_of_Booking).days+1
    total=days*instrument.instrument_price
    
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

def RentRequest(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)

    rentinstrument = Rentinstrument.objects.all()
    no_of_pending_request=count_pending_rent_request()
    return render(request,'Owner_RentRequest.html',{'owner':owner,'rentinstrument':rentinstrument,'no_of_pending_request':no_of_pending_request})

def SentRequests(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)

    no_of_pending_request=count_pending_rent_request()

    rentinstrument = Rentinstrument.objects.filter(customer_email=owner_email)
    if rentinstrument.exists():
        instrument = instrument.objects.all()
        return render(request,'Owner_SentRequests.html',{'owner':owner,'rentinstrument':rentinstrument,'instrument':instrument,'no_of_pending_request':no_of_pending_request})
    else:
        Message = "You haven't rented any instrument yet!!"
        return render(request,'Owner_SentRequests.html',{'owner':owner,'rentinstrument':rentinstrument,'Message':Message,'no_of_pending_request':no_of_pending_request})
    
    
# Create your views here.
def index(request):
    return render(request,'Rentinstrument/index.html')

def SendRequest_tolessor(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    user_email = request.session.get('user_email')

    Rentinstrument_Date_of_Booking=request.POST.get('Rentinstrument_Date_of_Booking','')
    Rentinstrument_Date_of_Return=request.POST.get('Rentinstrument_Date_of_Return','')
    Total_days=request.POST.get('Total_days','')
    Rentinstrument_Total_amount=request.POST.get('Rentinstrument_Total_amount','')
    instrument_license_plate=request.POST.get('instrument_license_plate','')
    Rentinstrument_Date_of_Booking=request.POST.get('Rentinstrument_Date_of_Booking','')
    Rentinstrument_Date_of_Booking = datetime.strptime(Rentinstrument_Date_of_Booking, "%b. %d, %Y").date()
    Rentinstrument_Date_of_Return = datetime.strptime(Rentinstrument_Date_of_Return, "%b. %d, %Y").date()
    
    rentinstrument = Rentinstrument(Rentinstrument_Date_of_Booking=Rentinstrument_Date_of_Booking,
    Rentinstrument_Date_of_Return=Rentinstrument_Date_of_Return,
    Total_days=Total_days,Rentinstrument_Total_amount=Rentinstrument_Total_amount,
    instrument_license_plate=instrument_license_plate,customer_email=user_email)

    rentinstrument.save()

    customer = Customer.objects.filter(customer_email=user_email)
    if customer.exists():
        return redirect("/SentRequests/")

    lessor = lessor.objects.filter(lessor_email=user_email)
    if lessor.exists():
        return redirect("/lessor/SentRequests/")

def AcceptRequest(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    user_email = request.session.get('user_email')
    id = request.GET.get('id','')
    rentinstrument = Rentinstrument.objects.get(id=id)
    rentinstrument.isAvailable= False
    rentinstrument.request_responded_by = user_email
    rentinstrument.request_status = "Accepted"
    rentinstrument.save()
    
    lessor = lessor.objects.filter(lessor_email=user_email)
    if lessor.exists():
        return redirect("/lessor/RentRequest/")

def DeclineRequest(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    user_email = request.session.get('user_email')
    id = request.GET.get('id','')
    rentinstrument = Rentinstrument.objects.get(id=id)
    rentinstrument.isAvailable= True
    rentinstrument.request_responded_by = user_email
    rentinstrument.request_status = "Declined"
    rentinstrument.save()    
    lessor = lessor.objects.filter(lessor_email=user_email)
    if lessor.exists():
        return redirect("/lessor/RentRequest/")

def CancelRequest(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    user_email = request.session.get('user_email')
    id = request.GET.get('id','')
    rentinstrument = Rentinstrument.objects.get(id=id)
    rentinstrument.delete()

    customer = Customer.objects.filter(customer_email=user_email)
    if customer.exists():
        return redirect("/SentRequests/")
    lessor = lessor.objects.filter(lessor_email=user_email)
    if lessor.exists():
        return redirect("/lessor/SentRequests/")