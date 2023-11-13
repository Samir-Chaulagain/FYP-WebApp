from django.shortcuts import get_object_or_404, render,redirect
from .forms import NewItemForm, EditItemForm

from .models import Item
from django.db.models import Q

# Create your views here.
def items(request):
    return render(request, 'explore/explore.html')
def upload_items(request):
    name=request.POST.get('instrument_name','')
    instrument_brand=request.POST.get('brand','')
    instrument_model=request.POST.get('model','')
    
    
    # instrument_uploaded_by=request.session.get('user_email')

    
    description=request.POST.get('description','')
    price=request.POST.get('price','')
    instrument_image1=request.FILES['instrument_image1']
    instrument_image2=request.FILES['instrument_image2']
    instrument_image3=request.FILES['instrument_image3']
    
    return render(request, 'explore/explore.html')
