
from .models import Post
import readline
from django.conf import settings
from django.http import HttpResponse

from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from . tokens import generate_token
from readline import get_current_history_length

def index(request):
    return render(request, 'landing_pages/index.html')

def about(request):
    return render(request, 'landing_pages/about.html')
def contact(request):
    return render(request, 'landing_pages/contact.html')

def blog(request):
    posts = Post.objects.all()
    return render(request, 'landing_pages/blog.html', {'posts': posts})


@csrf_protect
def signup(request):
    if request.method == "POST":
        
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
     
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('index')
        
     
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('index')
        
        
        
        myuser = User.objects.create_user(fname, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to MusicWorld!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to Muse rental Hub !! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nSamir"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        # current_site = get_current_history_length(request)

        # --------error----------
        readline = readline()  # Create a Readline object
        current_site = readline.get_current_history_length()
        email_subject = "Confirm your Email @ GFG - Django Login!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('index')
        
        
    return render(request, "landing_pages/signup.html")


# Create your views here.


def post(request, pk):
    posts = Post.objects.get(id=pk)
    return render(request, 'posts.html', {'posts': posts})
