

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
from explore.models import *

from django.shortcuts import render, get_object_or_404, redirect


from .models import Post

def index(request):
    posts = Post.objects.all()
    items = Item.objects.filter(is_sold=False)

    return render(request, 'landing_pages/index.html', {'posts': posts,'items':items})

def about(request):
    return render(request, 'landing_pages/about.html')


def events(request):

    return render(request, 'landing_pages/events.html')

def blog(request):
    posts = Post.objects.all()
    return render(request, 'landing_pages/blog.html', {'posts': posts})

def contact(request):
    return render(request, 'landing_pages/contact.html')

def post(request, pk):
    posts = Post.objects.get(id=pk)
    return render(request, 'posts.html', {'posts': posts})











    