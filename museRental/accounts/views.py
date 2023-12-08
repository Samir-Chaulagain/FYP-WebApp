
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
from accounts.permission import user_is_customer, user_is_lessor 

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
            next_url = request.GET.get('next', 'main:index')
            return redirect(next_url)
            # return render(request, "landing_pages/index.html",)
        else:
            messages.error(request, "Bad Credentials!!")
                
    
    return render(request,'accounts/login.html')

def user_logOut(request):
    """
    Provide the ability to logout
    """
    logout(request)
    return redirect('accounts:login')

def resetPassword(request):
    return render(request,'accounts/resetpass.html')

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_customer
def customer_edit_profile(request, id):

    """
    Handle customer Profile Update Functionality

    """

    user = get_object_or_404(User, id=id)
    form = CustomerProfileEditForm(request.POST or None, instance=user)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile Was Successfully Updated!')
            return redirect(reverse("accounts:edit-profile", kwargs={'id': id}))
    
    context = {
        'form': form
    }

    return render(request, 'accounts/edit-profile.html', context)

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_lessor
def lessor_edit_profile(request, id):

    """
    Handle customer Profile Update Functionality

    """

    user = get_object_or_404(User, id=id)
    form = CustomerProfileEditForm(request.POST or None, instance=user)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile Was Successfully Updated!')
            return redirect(reverse("accounts:edit-profile", kwargs={'id': id}))
    
    context = {
        'form': form
    }

    return render(request, 'accounts/edit-profile.html', context)




@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated...! Please log in with new password.')
            return redirect('accounts:login')
        
    else:
        form = ChangePasswordForm(user=request.user)

    return render(request, 'accounts/change_password.html', {'form': form})



