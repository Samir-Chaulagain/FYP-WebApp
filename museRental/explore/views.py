from email.message import EmailMessage
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.template.loader import render_to_string
from .forms import *
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .models import Item
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from accounts.models import User
from explore.forms import *
from explore.models import *
from accounts.permission import *

from datetime import datetime
User = get_user_model()


# Create your views here.

def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_published=True).order_by('-created_at')

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'explore/explore.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

# View instrument details
def showdetails(request,id):
    item = get_object_or_404(Item, id=id)
   

    return render(request, 'explore/details.html', {
        'item': item})

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_lessor
def add_item(request):
    """
    Provide the ability to create item post
    """
    form = additemForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    categories = Category.objects.all()

    if request.method == 'POST':

        if form.is_valid():

            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(
                    request, 'You have successfully posted your item! Please wait for review.')
            return redirect(reverse("explore:details", kwargs={
                                    'id': instance.id
                                    }))

    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'explore/add-instrument.html', context)




# def search_result_view(request):
#     """
#         User can search item with multiple fields

#     """

#     item = item.objects.order_by('-timestamp')

#     # Keywords
#     if 'item_name_or_created_by' in request.GET:
#         item_name_or_created_by = request.GET['item_name_or_created_by']

#         if item_name_or_created_by:
#             item = item.filter(title__icontains=item_name_or_created_by) | item.filter(
#                 company_name__icontains=item_name_or_created_by)

    # location
    # item Type
    # if 'item_type' in request.GET:
    #     item_type = request.GET['item_type']
    #     if item_type:
    #         item = item.filter(item_type__iexact=item_type)

    # return render(request, 'explore/result.html', item)


@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_customer
def rent_item_view(request, id):

    form = instrument_rent(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    Customers = Customer.objects.filter(user=user, item=id)

    if not Customers:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully applied for this item!')
                return redirect(reverse("explore:details", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("explore:details", kwargs={
                'id': id
            }))

    else:

        messages.error(request, 'You already applied for the item!')

        return redirect(reverse("explore:details", kwargs={
            'id': id
        }))
    
@login_required(login_url=reverse_lazy('accounts:login'))
def dashboard(request):
        
    items = []
    saveditems = []
    applieditems = []
    total_Customers = {}
    if request.user.role == 'lessor':
        items = Item.objects.filter(user=request.user.id)
    for item in items:
        count = Customer.objects.filter(item=item.id).count()
        total_Customers[item.id] = count
    if request.user.role == 'customer':
        saveditems = saved_item.objects.filter(user=request.user.id)
        applieditems = Customer.objects.filter(user=request.user.id)
    context = {
     'items': items,
        'saveditems': saveditems,
        'applieditems':applieditems,
        'total_Customers': total_Customers
    }
    return render(request, 'explore/dashboard.html', context)
@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_lessor
def all_Customers_view(request, id):

    all_Customers = Customer.objects.filter(item=id)

    context = {

        'all_Customers': all_Customers
    }

    return render(request, 'explore/all-customers.html', context)

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_lessor
def Customer_details_view(request, id):

    Customer = get_object_or_404(User, id=id)

    context = {

        'Customer': Customer
    }

    return render(request, 'explore/customer-details.html', context)

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_lessor
def delete_item_view(request, id):

    item = get_object_or_404(item, id=id, user=request.user.id)

    if item:

        item.delete()
        messages.success(request, 'Your item Post was successfully deleted!')

    return redirect('explore:dashboard')

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_lessor
def item_edit_view(request, id=id):
    """
    Handle item Update

    """

    item = get_object_or_404(item, id=id, user=request.user.id)
    categories = Category.objects.all()
    form = edititemForm(request.POST or None, instance=item)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # for save tags
        # form.save_m2m()
        messages.success(request, 'Your item Post Was Successfully Updated!')
        return redirect(reverse("explore:items", kwargs={
            'id': instance.id
        }))
    context = {

        'form': form,
        'categories': categories
    }

    return render(request, 'explore/item-edit.html', context)

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_lessor
def make_complete_item_view(request, id):
    item = get_object_or_404(item, id=id, user=request.user.id)

    if item:
        try:
            item.is_closed = True
            item.save()
            messages.success(request, 'Your item was marked closed!')
        except:
            messages.success(request, 'Something went wrong !')
            
    return redirect('explore:dashboard')

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_customer
def item_saved_view(request, id):
    form = ItemSavedForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    Customer = saved_item.objects.filter(user=request.user.id, item=id)

    if not Customer:
        if request.method == 'POST':
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(request, 'You have successfully saved this item!')
                return redirect(reverse("explore:details", kwargs={'id': id}))

        else:
            return redirect(reverse("explore:details", kwargs={'id': id}))

    else:
        messages.error(request, 'You already saved this item!')
        return redirect(reverse("explore:details", kwargs={'id': id}))

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_customer
def delete_save_view(request, id):

    item = get_object_or_404(saved_item, id=id, user=request.user.id)

    if item:
        item.delete()
        messages.success(request, 'Saved item was successfully deleted!')

    return redirect('explore:dashboard')


# contact USS

def contact_us(request):
    if request.method == 'POST':
        
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            try:
                # Prepare the HTML content of the email
                html_message = render_to_string('explore/mail.html', {'name': name})

                send_mail(
                    subject,
                    f'Name: {name}\nEmail: {email}\nMessage: {message}',
                    settings.EMAIL_HOST_USER,
                    ['remotejob007@gmail.com'],  # Replace with the recipient's email address
                    fail_silently=False,
                )

                send_mail(
                    'Message Received, Thanks for Contacting Us' ,
                    message,  # Plain text message, ignored if html_message is present
                    settings.EMAIL_HOST_USER,
                    [email],  # Use the email provided by the user in the form
                    fail_silently=False,
                    html_message=html_message,  # Pass the HTML content here
                )

                messages.success(request, 'Contact form has been successfully sent.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            messages.error(request, 'Fill out the form completely.')
    else:
        form = ContactForm()  # Create an empty form if the request method is GET
    
    return render(request, 'explore/contact.html')

# View to send email based on button type (select or reject)
def send_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        position = data.get('position')
        button_type = data.get('buttonType')

        # Send email based on button type (select or reject)
        subject = 'Application Status'
        template_name = 'explore/job_mail.html'
        context = {
            'position': position,
            'buttonType': button_type,
        }

        try:
            # Render the email content using the template and context
            email_content = render_to_string(template_name, context)
            # Send the email
            email = EmailMessage(subject, email_content, 'your@example.com', [email])
            email.content_subtype = "html"
            email.send()

            response_data = {'success': True, 'message': 'Email sent successfully!', 'buttonType': button_type}
        except Exception as e:
            print(str(e))
            response_data = {'success': False, 'message': 'Failed to send email.'}
        
        return JsonResponse(response_data)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})

