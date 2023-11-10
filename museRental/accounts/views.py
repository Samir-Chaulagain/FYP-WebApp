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

        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/customer_login/')

    else:
        form = CustomerRegistrationForm()

    return render(request, 'accounts/customer-registration.html', {
        'form': form
    })


def lessor_registration(request):
    if request.method == 'POST':

        form = LessorRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/lessor_login/')

    else:
        form = LessorRegistrationForm()

    return render(request, 'accounts/lessor-registration.html', {
        'form': form
    })






def customer_logOut(request):
    """
    Provide the ability to logout
    """
    auth.logout(request)
    messages.success(request, 'You are Successfully logged out')
    return redirect('accounts:customer_login')

def lessor_logOut(request):
    """
    Provide the ability to logout
    """
    auth.logout(request)
    messages.success(request, 'You are Successfully logged out')
    return redirect('accounts:lessor_login')