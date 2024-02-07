

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from .forms import ContactForm
import json

from explore.models import *
from event.models import *

from django.shortcuts import render


from .models import Post

def index(request):
    posts = Post.objects.all()
    items = Item.objects.filter(is_sold=False)
    events = Event.objects.all()

    return render(request, 'landing_pages/index.html', {'posts': posts,'items':items , 'events': events})

def about(request):
    return render(request, 'landing_pages/about.html')


def events(request):

    return render(request, 'landing_pages/events.html')

# contact USS

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            try:
                # Prepare the HTML content of the email
                html_message = render_to_string('landing_pages/mail.html', {'name': name})

                send_mail(
                    subject,
                    f'Name: {name}\nEmail: {email}\nMessage: {message}',
                    settings.EMAIL_HOST_USER,
                    ['muserentalhub@gmail.com'],  # Replace with the recipient's email address
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
    
    return render(request, 'landing_pages/contact.html',{'form': form})

# View to send email based on button type (select or reject)
def send_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        position = data.get('position')
        button_type = data.get('buttonType')

        # Send email based on button type (select or reject)
        subject = 'Application Status'
        template_name = 'explore/item_mail.html'
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


def blog(request):
    posts = Post.objects.all()
    return render(request, 'landing_pages/blog.html', {'posts': posts})


def post(request, pk):
    posts = Post.objects.get(id=pk)
    return render(request, 'landing_pages/posts.html', {'posts': posts})











    