from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse, reverse_lazy

from .forms import *
from .permission import user_is_customer 



def customer_registration(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)  # Ensure request.FILES is passed
        if form.is_valid():
            user = form.save(commit=False)
            
            user.save()
            messages.success(request, 'Your Profile Was Successfully Created!')
            return redirect('accounts:login')
    else:
        form = CustomerRegistrationForm()
# 
    context = {
        'form': form
    }

    return render(request, 'accounts/customer-registration.html', context)


def lessor_registration(request):
    if request.method == 'POST':
        form = LessorRegistrationForm(request.POST)  # Include request.FILES to handle file uploads
        if form.is_valid():
            lessor = form.save(commit=False)
            lessor.save()
            messages.success(request, 'Your Profile Was Successfully Created!')
            return redirect('accounts:login')
    else:
        form = LessorRegistrationForm()

    context = {
        'form': form
    }

    return render(request, 'accounts/lessor-registration.html', context)

def user_logIn(request):

    """
    Provides users to logIn

    """

    form = UserLoginForm(request.POST or None)
    

    if request.user.is_authenticated:
        return redirect('/')
    
    else:
        if request.method == 'POST':
            if form.is_valid():
                auth.login(request, form.get_user())
                return HttpResponseRedirect(get_success_url(request))
    context = {
        'form': form,
    }

    return render(request,'accounts/login.html',context)


def user_logOut(request):
    """
    Provide the ability to logout
    """
    auth.logout(request)
    messages.success(request, 'You are Successfully logged out')
    return redirect('accounts:login')