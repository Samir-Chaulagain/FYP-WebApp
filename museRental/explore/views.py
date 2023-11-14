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

# Create your views here.
def items(request):
    return render(request, 'explore/explore.html')

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
