

import os
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.template.loader import render_to_string

from accounts import apps

from .forms import *
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .models import Item
from django.db.models import Q, Avg
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from accounts.models import User
from explore.forms import *
from explore.models import *
from event.models import saved_event,Booking
from accounts.permission import *
import json

import logging
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from datetime import datetime, date
from .models import Customer, Item
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from xhtml2pdf import pisa



from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
import os
from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import send_mail
import json
import datetime
from django.utils import timezone
from .models import Customer

from datetime import date, datetime



import os
import json
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.units import inch
from PIL import Image as PILImage
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.http import JsonResponse
User = get_user_model()


# Create your views here.

#items function to display/render explore page 
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Item, Category

def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    item_type = request.GET.get('item_type', '')  # Get the item type from the query parameters

    categories = Category.objects.all()
    item_list = Item.objects.filter(is_published=True, is_sold=False).order_by('-created_at')

    # Apply category filter
    if category_id:
        item_list = item_list.filter(category_id=category_id)

    # Apply query filter
    if query:
        item_list = item_list.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Apply item type filter
    if item_type:
        item_list = item_list.filter(item_type=item_type)

    paginator = Paginator(item_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'explore/explore.html', {
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        'page_obj': page_obj,
        'items': page_obj,  # Pass paginated items instead of the whole item_list
    })


# View instrument details
def showdetails(request, id):
    item = get_object_or_404(Item, id=id)
    
    # Manually create tags based on the category field of the item
  
    
    # Get related items based on the created tags
    related_item_list = Item.objects.filter(category=item.category).exclude(id=item.id)
    # Paginate related items
    paginator = Paginator(related_item_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get reviews for the item
    reviews = Review.objects.filter(item=item) 
    # Calculate average rating for the item
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    context = {
        'item': item,
        'page_obj': page_obj,
        'total': len(related_item_list),
        'reviews': reviews,
        'average_rating': average_rating
    }
    return render(request, 'explore/details.html', context)

    return render(request, 'explore/details.html', context)



@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_customer
def rate_item(request, id):
    if request.method == 'POST':
        val = request.POST.get('val')
        comment = request.POST.get('comment')
        item = get_object_or_404(Item, id=id)
        user = request.user

        if not val:  # Check if val is empty
            return JsonResponse({'success': False, 'error': 'Rating value is missing'}, status=400)

        rating = int(val)

        # Check if the user has already rated the item
        try:
            rating_review = Review.objects.get(item=item, user=user)
            rating_review.rating = rating
            rating_review.comment = comment
            rating_review.save()
        except Review.DoesNotExist:
            # Create a new rating if the user has not rated the item yet
            rating_review = Review.objects.create(item=item, user=user, rating=rating, comment=comment)

        # Redirect the user to the details page of the item
        return redirect('explore:details', id=item.id)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_lessor
def add_item(request):
    # Provide the ability to create item post
    form = additemForm(request.POST or None, request.FILES or None)

    user = get_object_or_404(User, id=request.user.id)
    categories = Category.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            item = form.save(commit=False)
            item.latitude = request.POST.get('latitude')
            item.longitude = request.POST.get('longitude')
            item.save()


            # Save tags
            form.save_m2m()
            # Loop through each uploaded file and associate it with the created item
            for file in request.FILES.getlist('file'):
                # Create an Image instance and associate it with the created item
                Image.objects.create(item=instance, image=file)
            

            messages.success(
                request, 'You have successfully posted your item! Please wait for review.')
            
            
    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'explore/add-instrument.html', context)


@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_lessor
def item_edit_view(request, id=id):
    # Delete existing images
    item = get_object_or_404(Item, id=id, user=request.user.id)
    categories = Category.objects.all()
    form = edititemForm(request.POST or None,request.FILES or None, instance=item)
    if form.is_valid():
        item.image_set.all().delete()
        instance = form.save(commit=False)
        
        item.latitude = request.POST.get('latitude')
        item.longitude = request.POST.get('longitude')
        item.save()
        print(item.latitude,item.longitude)
        
        for file in request.FILES.getlist('file'):
                # Create an Image instance and associate it with the created item

                Image.objects.create(item=instance, image=file)
        
        # Save the instance first to get the updated ID
        
        
      
    

        
        messages.success(request, 'Your item post was successfully updated! Please check your dashboard.')
        return redirect(reverse("explore:edit-item", kwargs={'id': instance.id}))
    
    context = {
        'form': form,
        'categories': categories,
        'item': item,
    }

    return render(request, 'explore/item-edit.html', context)



@login_required(login_url=reverse_lazy('accounts:login'))
def dashboard(request):
        
    items = []
    saveditems = []
    savedevent = []
    applieditems = []
    appliedevent = []
    total_Customers = {}
    if request.user.role == 'lessor':
        items = Item.objects.filter(user=request.user.id)
    for item in items:
        count = Customer.objects.filter(item=item.id).count()
        total_Customers[item.id] = count
    if request.user.role == 'customer':
        saveditems = saved_item.objects.filter(user=request.user.id)
        applieditems = Customer.objects.filter(user=request.user.id)
        savedevent=saved_event.objects.filter(user=request.user.id)
        appliedevent=Booking.objects.filter(user=request.user.id)

    if request.user.role == 'lessor':
        savedevent=saved_event.objects.filter(user=request.user.id)
        appliedevent=Booking.objects.filter(user=request.user.id)
    
    context = {
     'items': items,
        'saveditems': saveditems,
        'applieditems':applieditems,
        'total_Customers': total_Customers,
        'savedevent': savedevent,
        'appliedevent': appliedevent,
        
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
def delete_item(request, id):

    item = get_object_or_404(Item, id=id, user=request.user.id)

    if item:

        item.delete()
        messages.success(request, 'Your item post was successfully deleted!')

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

                messages.success(request, 'You have successfully saved this item!! Please Check Your Dashboard')
                return redirect(reverse("explore:details", kwargs={'id': id}))

        else:
            return redirect(reverse("explore:details", kwargs={'id': id}))

    else:
        
        return redirect(reverse("explore:details", kwargs={'id': id}))

# details
@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_customer
def delete_save_view(request, id):

    item = saved_item.objects.filter(item=id, user=request.user).first()


    if item:
        item.delete()
        messages.success(request, 'Saved item was successfully removed! Please check your dashboard.')

    return redirect('explore:details', id=id)


# Dashboard
@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_customer
def deletesaveditem(request, id):
    

    item = get_object_or_404(saved_item, id=id, user=request.user.id)

    if item:
        item.delete()
        messages.success(request, 'Saved item was successfully deleted! Please check your dashboard.')

    return redirect('explore:dashboard')





# from .decorators import user_is_customer

@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_customer
def CheckAvailability(request, id):
    customer = Customer.objects.filter(user=request.user.id, item_id=id)
    
    Rentitem_Date_of_Booking = request.POST.get('Rentitem_Date_of_Booking', '')
    Rentitem_Date_of_Return = request.POST.get('Rentitem_Date_of_Return', '')
    
    Rentitem_Date_of_Booking = datetime.strptime(Rentitem_Date_of_Booking, '%Y-%m-%d').date()
    Rentitem_Date_of_Return = datetime.strptime(Rentitem_Date_of_Return, '%Y-%m-%d').date()

    item = Item.objects.get(id=id)

    if Rentitem_Date_of_Booking < date.today():
        Incorrect_dates = "Please give proper dates"
        return render(request, 'explore/details.html', {'Incorrect_dates': Incorrect_dates, 'item': item})

    if Rentitem_Date_of_Return < Rentitem_Date_of_Booking:
        Incorrect_dates = "Please give proper dates"
        return render(request, 'explore/details.html', {'Incorrect_dates': Incorrect_dates, 'item': item})
    
    rentItem = Customer.objects.filter(item_id=id, isAvailable=True)
    
    for i in rentItem:
        if (Rentitem_Date_of_Booking <= i.Rentitem_Date_of_Return and Rentitem_Date_of_Return >= i.Rentitem_Date_of_Booking):

            # Overlapping date range with an available item
            NotAvailable = True
            Message = "Note that somebody has also requested for this item from " + str(i.Rentitem_Date_of_Booking) + " to " + str(i.Rentitem_Date_of_Return)+" So there are some chances that you might not get it. As items are rented on First come first serve policy."
            messages.error(request, Message)
            # rent_data = {"Rentitem_Date_of_Booking": Rentitem_Date_of_Booking, "Rentitem_Date_of_Return": Rentitem_Date_of_Return, "days": (Rentitem_Date_of_Return - Rentitem_Date_of_Booking).days + 1, "total": item.price * ((Rentitem_Date_of_Return - Rentitem_Date_of_Booking).days + 1)}
            return render(request, 'explore/details.html', {'Message': Message, 'NotAvailable': NotAvailable, 'item': item, 'customer': customer})
    
    # No overlapping date ranges found, the item is available
    Available = True
    Message = "Items available to book for the given date range"

    rent_data = {"Rentitem_Date_of_Booking": Rentitem_Date_of_Booking, "Rentitem_Date_of_Return": Rentitem_Date_of_Return, "days": (Rentitem_Date_of_Return - Rentitem_Date_of_Booking).days + 1, "total": item.price * ((Rentitem_Date_of_Return - Rentitem_Date_of_Booking).days + 1)}
    return render(request, 'explore/details.html', {'Message': Message,'Available': Available, 'item': item, 'customer': customer, 'rent_data': rent_data})

import random
from django.utils.crypto import get_random_string
def generate_invoice_number():
    prefix = "MRH"  # Prefix for the invoice number
    random_int = random.randint(10000, 99999)  # Generate a random integer between 10000 and 99999
    suffix = "IRS"  # Suffix for the invoice number
    print(f"{prefix}{random_int}{suffix}")
    return f"{prefix}{random_int}{suffix}"


@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_customer
def rent_item_view(request, id):
    user = get_object_or_404(User, id=request.user.id)
    Customers = Customer.objects.filter(user=user, item=id)
    
    if not Customers:
        if request.method == 'POST':
            Rentitem_Date_of_Booking = request.POST.get('Rentitem_Date_of_Booking', '')
            Rentitem_Date_of_Return = request.POST.get('Rentitem_Date_of_Return', '')
            latitude = request.POST.get('latitude','')
            longitude = request.POST.get('longitude','')
            time = request.POST.get('time','')
            invoice_number = generate_invoice_number()
            

            Rentitem_Date_of_Booking = datetime.strptime(Rentitem_Date_of_Booking, '%B %d, %Y').date()
            Rentitem_Date_of_Return = datetime.strptime(Rentitem_Date_of_Return, '%B %d, %Y').date()

            item = get_object_or_404(Item, id=id)
            total_days = (Rentitem_Date_of_Return - Rentitem_Date_of_Booking).days + 1
            total_amount = total_days * item.price

            instance = Customer(
                user=user,
                item=item,
                Rentitem_Date_of_Booking=Rentitem_Date_of_Booking,
                Rentitem_Date_of_Return=Rentitem_Date_of_Return,
                Total_days=total_days,
                Rentitem_Total_amount=total_amount,
                latitude=latitude,
                longitude=longitude,
                time=time,
                invoice_number=invoice_number,
                

            )
            context = {
                'invoice_number': invoice_number,
                # Add other data to the context as needed
            }
        

            instance.save()
            
            messages.success(request, 'You have successfully rented this item! Please check your dashboard.')
            return redirect(reverse("explore:details", kwargs={'id': id}),context)

    else:
        messages.error(request, 'You already applied for the item! Please check your dashboard')

    return redirect(reverse("explore:details", kwargs={'id': id}),context)
    




# Get or create a logger for this module
logger = logging.getLogger(__name__)

# Decorators to exempt CSRF protection and require POST method for this view
@csrf_exempt
def send_email_after_payment(request):
    data = json.loads(request.body)
    lessor_email = data.get('lessor_email')
    customer_email = data.get('customer_email')
    bookingdate = data.get('bookingdate')
    returndate = data.get('returndate')
    days = data.get('days')
    amt = data.get('amt')
    name = data.get('name')
    tenant_name = data.get('tenant_name')
    customer_name = data.get('customer_name')
    time = data.get('time')
    invoice_number = generate_invoice_number()
    
    
    

    context = {
        'bookingdate': bookingdate,
        'returndate': returndate,
        'days': days,
        'amt': amt,
        'name': name,
        'tenant_name': tenant_name,
        "lessor_email": lessor_email,
        'customer_email': customer_email,
        'customer_name': customer_name,
        'invoice': invoice_number,
        'time': time,
        'request': request  # Passing request object in the context
    }
    print('1234'+invoice_number)
    print("hi")
    # Render the template
    html = render_to_string('landing_pages/invoice_template.html', context)
    print("h2")

    # Create a PDF file
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    # Check if there were any errors during PDF creation
    if not pdf.err:
        # PDF created successfully, proceed with sending emails
        print("h3")
        filename = 'Invoice.pdf'
        subject = 'Payment Successful'

        # Send email to lessor
        lessor_email_message = EmailMessage(subject, 'Please find invoice attached with this email.', 'muserentalhub@gmail.com', [lessor_email])
        lessor_email_message.attach(filename, result.getvalue(), 'application/pdf')
        lessor_email_message.send()

        # Send email to customer
        customer_email_message = EmailMessage(subject, 'Payment Receipt, Congratulations! You have successfully rented . You will have your desired instrument by the time . Thank you! Here are the details:', 'muserentalhub@gmail.com', [customer_email])
        customer_email_message.attach(filename, result.getvalue(), 'application/pdf')
        customer_email_message.send()

        return JsonResponse({'status': 'success'})
    else:
        # There was an error creating the PDF
        return JsonResponse({'status': 'error', 'message': 'Error creating PDF'}, status=500)


# def send_email_after_payment(request):
#     try:
#         data = json.loads(request.body)
#         lessor_email = data.get('lessor_email')
#         customer_email = data.get('customer_email')

#         subject = 'Payment Successful'
#         from_email = 'muserentalhub@gmail.com'

#         # Load HTML templates and render with context
#         lessor_html_message = render_to_string('explore/lessor_email_after_payment.html')
#         customer_html_message = render_to_string('explore/customer_email_after_payment.html')

#         # Generate PDF attachment
#         pdf_buffer = BytesIO()

#         # Create a PDF document with a table
#         doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
#         table_data = [['', 'Column 2', 'Column 3'],
#                       ['Row 1 Data 1', 'Row 1 Data 2', 'Row 1 Data 3'],
#                       ['Row 2 Data 1', 'Row 2 Data 2', 'Row 2 Data 3']]
#         table = Table(table_data)
#         style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                             ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#                             ('GRID', (0, 0), (-1, -1), 1, colors.black)])
#         table.setStyle(style)
#         doc.build([table])

#         # Move the buffer pointer to the beginning to read the PDF content
#         pdf_buffer.seek(0)

#         # Create EmailMessage objects for both lessor and customer
#         lessor_email_message = EmailMessage(subject, lessor_html_message, from_email, [lessor_email])
#         lessor_email_message.attach('table_data.pdf', pdf_buffer.getvalue(), 'application/pdf')
#         lessor_email_message.content_subtype = 'html'
#         lessor_email_message.send()

#         customer_email_message = EmailMessage(subject, customer_html_message, from_email, [customer_email])
#         customer_email_message.attach('table_data.pdf', pdf_buffer.getvalue(), 'application/pdf')
#         customer_email_message.content_subtype = 'html'
#         customer_email_message.send()

#         return JsonResponse({'status': 'success'})
#     except Exception as e:
#         logger.error(f"Error sending email: {e}")
#         return JsonResponse({'status': 'error'}, status=500)





# def send_email_after_payment(request):
#     try:
#         data = json.loads(request.body)
#         lessor_email = data.get('lessor_email')
#         customer_email = data.get('customer_email')

#         # Retrieve customer details to include in the invoice PDF
#         customer = Customer.objects.get(user__email=customer_email)
#         invoice_data = {
#             'invoice':customer.invoice,
#             'booking_date': customer.Rentitem_Date_of_Booking,
#             'return_date': customer.Rentitem_Date_of_Return,
#             'total_days': customer.Total_days,
#             'total_amount': customer.Rentitem_Total_amount,
#             'created_at': customer.created_at,
#             'time': customer.time,
#         }

#         # Render the HTML template for the invoice
#         invoice_html = render_to_string('landing_pages/invoice_template.html', invoice_data)

#         # Generate PDF from HTML template
#         pdf_file_path = os.path.join(settings.BASE_DIR, 'invoice.pdf')
#         html_template = get_template('landing_pages/invoice_template.html')
#         rendered_html = html_template.render(invoice_data)

#         # Write rendered HTML to PDF file
#         import pdfkit
#         pdfkit.from_string(rendered_html, pdf_file_path)

#         subject = 'Payment Successful'
#         from_email = 'muserentalhub@gmail.com'

#         # Load HTML templates and render with context
#         lessor_html_message = render_to_string('explore/lessor_email_after_payment.html')
#         customer_html_message = render_to_string('explore/customer_email_after_payment.html')

#         # Send email to the lessor with lessor_html_message and attach the PDF
#         msg_to_lessor = EmailMultiAlternatives(subject, '', from_email, [lessor_email])
#         msg_to_lessor.attach_alternative(lessor_html_message, "text/html")
#         with open(pdf_file_path, 'rb') as pdf_file:
#             msg_to_lessor.attach('invoice.pdf', pdf_file.read(), 'application/pdf')
#         msg_to_lessor.send()

#         # Send email to the customer with customer_html_message and attach the PDF
#         msg_to_customer = EmailMultiAlternatives(subject, '', from_email, [customer_email])
#         msg_to_customer.attach_alternative(customer_html_message, "text/html")
#         with open(pdf_file_path, 'rb') as pdf_file:
#             msg_to_customer.attach('invoice.pdf', pdf_file.read(), 'application/pdf')
#         msg_to_customer.send()

#         return JsonResponse({'status': 'success'})
#     except Exception as e:
#         logger.error(f"Error sending email: {e}")
#         return JsonResponse({'status': 'error'}, status=500)








@require_POST
@csrf_exempt  # CSRF exemption for simplicity; consider using a decorator like csrf_protect in production
def update_status(request):
    user_id = request.POST.get('user_id')
    new_status = request.POST.get('new_status')
    print(new_status)
    
    customer = Customer.objects.get(id=user_id)
    customer.request_status = new_status
    customer.save()
    
    messages.success(request, 'Status updated successfully!')
    return JsonResponse({'status': 'success'})
    



