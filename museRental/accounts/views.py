from pyexpat.errors import messages
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.


def SignupPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        phonenumber=request.POST.get('phonenumber')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(username=username,  # Use email as the username
                email=email,
                password=pass1,
                first_name=fname,
                last_name=lname)
            my_user.save()
            return redirect('login')
        
    return render (request,'accounts/signup.html')


def LoginPage(request):
    if request.method=='POST':
        email=request.POST.get('email')
        pass1=request.POST.get('pass')
        user=authenticate(request,email=email,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('main:index')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'accounts/login.html')

def LogoutPage(request):
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
