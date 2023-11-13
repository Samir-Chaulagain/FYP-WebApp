
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect , get_object_or_404

from django.urls import reverse, reverse_lazy
# importing forms and views
from .forms import *
from main.views import *
from .models import User

# getting permission
from .permission import user_is_customer, user_is_lessor 

# for loginrequired
from django.contrib.auth.decorators import login_required



def customer_registration(request):

    
    form = CustomerRegistrationForm(request.POST or None)
    if form.is_valid():
        form = form.save()
        return redirect('accounts:login')
    context={
        
            'form':form
        }


    return render(request,'accounts/customer-registration.html',context)




def lessor_registration(request):
   
    form = LessorRegistrationForm(request.POST or None)
    if form.is_valid():
        form = form.save()
        return redirect('accounts:login')
    context={
        
            'form':form
        }

    return render(request,'accounts/lessor-registration.html',context)


def user_logIn(request):

    if request.method == 'POST':

        email = request.POST['email']
        pass1 = request.POST['password']
        
        user = authenticate(email=email, password=pass1)
        
        if user is not None:
            login(request, user)
            
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "landing_pages/index.html",)
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('main:blog')    
    

    return render(request,'accounts/login.html')

def user_logOut(request):
    """
    Provide the ability to logout
    """
    logout(request)
    return redirect('login')

def resetPassword(request):
    return render(request,'accounts/resetpass.html')

@user_is_lessor
# ADD ITEMS
def upload_instrument(request):
    if('email' not in request.session):
        return redirect('/signin/')
    email = request.session.get('email')
    lessor_email= User.objects.get(Owner_email=email)
    
    return render(request,"explore/add-instrument.html",{'owner':lessor_email})
# Edit Items
# Manage items
# Views 


# Create Packages
