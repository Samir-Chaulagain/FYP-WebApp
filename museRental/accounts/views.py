from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse, reverse_lazy

from .forms import *
from accounts.views import *
from .permission import user_is_customer 



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
        username = request.POST['email']
        pass1 = request.POST['password']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "landing_pages/index.html")
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('main:index')
    
    

    return render(request,'accounts/customer-login.html')



# def get_success_url(request):

#     """
#     Handle Success Url After LogIN

#     """
#     if 'next' in request.GET and request.GET['next'] != '':
#         return request.GET['next']
#     else:
#         return reverse('main:index')   


def user_logOut(request):
    """
    Provide the ability to logout
    """
    auth.logout(request)
    messages.success(request, 'You are Successfully logged out')

    return redirect('accounts:login')

