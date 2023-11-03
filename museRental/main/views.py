

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

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewItemForm, EditItemForm
from .models import Category, Item,Post

def index(request):
    return render(request, 'landing_pages/index.html')

def about(request):
    return render(request, 'landing_pages/about.html')
def explore(request):
    return render(request, 'landing_pages/explore.html')

def events(request):
    return render(request, 'landing_pages/events.html')

def blog(request):
    posts = Post.objects.all()
    return render(request, 'landing_pages/blog.html', {'posts': posts})

def contact(request):
    return render(request, 'landing_pages/contact.html')


# def 





# Create your views here.


def post(request, pk):
    posts = Post.objects.get(id=pk)
    return render(request, 'posts.html', {'posts': posts})





def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'landing_pages/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'landing_pages/detail.html', {
        'item': item,
        'related_items': related_items
    })


def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('main:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'landing_pages/form.html', {
        'form': form,
        'title': 'New item',
    })


def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('main:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'landing_pages/form.html', {
        'form': form,
        'title': 'Edit item',
    })


def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('index')
    