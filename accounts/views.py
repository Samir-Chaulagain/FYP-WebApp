
from django.contrib.auth.tokens import default_token_generator
from .models import User  # Import the custom User model


from django.contrib.auth import login
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse, reverse_lazy
# importing forms and views
from .forms import *
from main.views import *

# getting permission
from accounts.permission import user_is_customer, user_is_lessor 
# for loginrequired
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site



# Customer REgistration and ativtion via mail
def customer_registration(request):   
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set the user as inactive until email confirmation
            user.save()

            # Determine the protocol based on the request
            protocol = 'https' if request.is_secure() else 'http'

            # Send email verification
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'protocol': protocol,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(subject, message, to=[to_email])
            email.content_subtype = "html"
            email.send()

            try:
                email.send()
                messages.success(request, 'Please check your email to activate your account.')
            except Exception as e:
                # Log the exception or handle it appropriately
                messages.error(request, 'There was an error sending the activation email. Please try again.')

            return redirect('accounts:login')
    else:
        form = CustomerRegistrationForm()
    context={
            
                'form':form
            }
    return render(request,'accounts/customer-registration.html',context)

# TO Actvate User function for mail
def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)  # Use the custom User model
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated. Please login.")
        return redirect('accounts:login')  # Redirect to the login page
    else:
        messages.error(request, "Invalid Link. Please try again or contact support.")
        return redirect('accounts:login') 
    

# Lessor Registration view function
def lessor_registration(request):
    if request.method == 'POST':
        form = LessorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set the user as inactive until email confirmation
            user.save()

            # Determine the protocol based on the request
            protocol = 'https' if request.is_secure() else 'http'

            # Send email verification
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'protocol': protocol,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(subject, message, to=[to_email])
            email.content_subtype = "html"
            email.send()

            try:
                email.send()
                messages.success(request, 'Please check your email to activate your account.')
            except Exception as e:
                # Log the exception or handle it appropriately
                messages.error(request, 'There was an error sending the activation email. Please try again.')

            return redirect('accounts:login')
    
    
    else:
        form = LessorRegistrationForm()
    context={       
            'form':form
        }

    return render(request,'accounts/lessor-registration.html',context)


# User Login function
def user_logIn(request):

    if request.user.is_authenticated:
        # User is already logged in, redirect to the main page
        return render(request, 'landing_pages/index.html')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me') == 'on'

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            # Remeber me in session 

            if remember_me:
                request.session.set_expiry(2592000)
            else:
                request.session.set_expiry(0)

            next_url = request.GET.get('next', 'main:index')
             # Display SweetAlert for login success
            messages.success(request, 'Login successful!')
            
            return redirect(next_url)
        else:
            # Use the messages framework to display an error message
            messages.error(request, 'Invalid email or password. Please try again.')
    
    return render(request, 'accounts/login.html')


# Logout Function
def user_logOut(request):
    """
    Provide the ability to logout
    """
    logout(request)
    return redirect('accounts:login')


    
# Customer edit Profile
@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_customer
def customer_edit_profile(request, id):

    """
    Handle customer Profile Update Functionality

    """

    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        ChangePasswordForm1= ChangePasswordForm(user=request.user, data=request.POST)
        if ChangePasswordForm1.is_valid():
            ChangePasswordForm1.save()
            messages.success(request, 'Your password was successfully updated...! Please log in with new password.')
            return redirect('accounts:login')
        
    else:
        ChangePasswordForm1 = ChangePasswordForm(user=request.user)
    
    if request.method == 'POST':
        form = CustomerProfileEditForm(request.POST , request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile Was Successfully Updated!')
            return redirect(reverse("accounts:customer-edit-profile", kwargs={'id': id}))
    else:
        form = CustomerProfileEditForm(instance=user)

    
    context = {
        'form': form,
        'form1':ChangePasswordForm1
    }

    return render(request, 'accounts/customer-edit-profile.html', context)


# Lessor EDit Form
@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_lessor
def lessor_edit_profile(request, id):

    """
    Handle customer Profile Update Functionality



    """

    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        ChangePasswordForm1= ChangePasswordForm(user=request.user, data=request.POST)
        if ChangePasswordForm1.is_valid():
            ChangePasswordForm1.save()
            messages.success(request, 'Your password was successfully updated...! Please log in with new password.')
            return redirect('accounts:login')
        
    else:
        ChangePasswordForm1 = ChangePasswordForm(user=request.user)
    

    if request.method == 'POST':
        form = LessorProfileEditForm(request.POST , request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Profile Successfully!!')
            return redirect(reverse("accounts:customer-edit-profile", kwargs={'id': id}))
    else:
        form = LessorProfileEditForm(instance=user)

    
    context = {
        'form': form,
        'form1':ChangePasswordForm1,
    }

    return render(request, 'accounts/customer-edit-profile.html', context)







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





