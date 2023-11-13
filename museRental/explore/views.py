from django.shortcuts import get_object_or_404, render,redirect
from .forms import NewItemForm, EditItemForm

from .models import Category, Item
from django.db.models import Q

# Create your views here.
def items(request):
    return render(request, 'explore/explore.html')
def upload_items(request):

    
    return render(request, 'explore/explore.html')
