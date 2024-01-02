
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import authenticate, login, logout
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
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            form = form.save()
            return redirect('accounts:login')
    else:
        form = CustomerRegistrationForm()
    context={
            
                'form':form
            }
    return render(request,'accounts/customer-registration.html',context)

def lessor_registration(request):
    if request.method == 'POST':
        form = LessorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save()
            return redirect('accounts:login')
    
    
    else:
        form = LessorRegistrationForm()
    context={       
            'form':form
        }

    return render(request,'accounts/lessor-registration.html',context)

def user_logIn(request):
    message=None
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me') == 'on'  # Check if the "Remember Me" checkbox is selected

        user = authenticate(request, email=email, password=password)

        if user is not None:
            
            login(request, user)

            # Set session expiration time based on "Remember Me" checkbox
            if remember_me:
                # Set a longer session expiration time, e.g., 1 month (in seconds)
                request.session.set_expiry(2592000)  # 1 month in seconds
            else:
                # Use the default session expiration time (settings.SESSION_COOKIE_AGE)
                request.session.set_expiry(0) 
                pass
            
            next_url = request.GET.get('next', 'main:index')
            return redirect(next_url)
        
    else:
        # Optionally, you can add a success message here
        # messages.success(request, 'Form submitted successfully!')
          # Exa 
        message= 'Invalid error password or mail'

    return render(request, 'accounts/login.html',{'message':message})


def user_logOut(request):
    """
    Provide the ability to logout
    """
    logout(request)
    return redirect('accounts:login')


    

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_customer
def customer_edit_profile(request, id):

    """
    Handle customer Profile Update Functionality

    """

    user = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        form = CustomerProfileEditForm(request.POST , request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile Was Successfully Updated!')
            return redirect(reverse("accounts:customer-edit-profile", kwargs={'id': id}))
    else:
        form = CustomerProfileEditForm(instance=user)

    
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
    form = CustomerProfileEditForm(request.POST, request.FILES, instance=user)
    
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


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:login')  #  the login URL

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Add a success message
        messages.success(self.request, 'Password reset successful. You can now log in with your new password.')

        return response

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'





