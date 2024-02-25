

from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .forms import ContactForm, DisputeForm
from django.core.paginator import Paginator



from explore.models import *
from event.models import *

from django.shortcuts import render


from .models import Dispute, Post

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
    # Handling POST request
    if request.method == 'POST':
        # Creating a ContactForm instance with the POST data
        form = ContactForm(request.POST)
        # Validating the form
        if form.is_valid():
            # Extracting cleaned data from the form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            try:
                # Rendering HTML content for the email using a template
                html_message = render_to_string('landing_pages/conactmail.html', {'name': name})

                # Sending an email notification to the site owner/administrator
                send_mail(
                    subject,
                    f'Name: {name}\nEmail: {email}\nMessage: {message}',
                    settings.EMAIL_HOST_USER,
                    ['muserentalhub@gmail.com'],  # Replace with the recipient's email address
                    fail_silently=False,
                )

                # Sending an acknowledgment email to the sender
                send_mail(
                    'Message Received, Thanks for Contacting Us',
                    message,  # Plain text message, ignored if html_message is present
                    settings.EMAIL_HOST_USER,
                    [email],  # Use the email provided by the user in the form
                    fail_silently=False,
                    html_message=html_message,  # Pass the HTML content here
                )

                # Displaying success message if emails are sent successfully
                messages.success(request, 'Contact form has been successfully sent.')
            except Exception as e:
                # Handling exceptions if email sending fails
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            # Displaying error message if the form is not valid
            messages.error(request, 'Fill out the form completely.')
    else:
        # Handling GET request
        form = ContactForm()  # Create an empty form if the request method is GET
    
    # Rendering the 'contact.html' template with the form
    return render(request, 'landing_pages/contact.html', {'form': form})



# creating dispute
def dispute(request):
    if request.method == 'POST':
        form = DisputeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            invoice = form.cleaned_data['invoice']
            issue = form.cleaned_data['issue']
            
            # Save the dispute information to the database
            dispute = Dispute.objects.create(
                name=name,
                email=email,
                invoice=invoice,
                issue=issue
            )
            
            # Send email to muserentalhub and user
            try:
                # Email content for muserentalhub
                hub_html_message = render_to_string('landing_pages/dispute_mail.html', {
                    'name': name,
                    'subject': invoice,
                    'message': issue
                })
                
                send_mail(
                    invoice,  # subject
                    issue,  # message
                    settings.EMAIL_HOST_USER,  # sender email
                    ['muserentalhub@gmail.com'],  # receiver email
                    fail_silently=False,
                    html_message=hub_html_message  # HTML message
                )
                
                # Email content for user
                user_html_message = render_to_string('landing_pages/mail.html', {
                    'name': name,
                    'subject': 'Message Received, Thanks for Contacting Us',
                    'message': 'We have received your dispute information. We will get back to you as soon as possible.'
                })
            
                send_mail(
                    'Message Received, Thanks for Contacting Us',  # subject
                    'We have received your dispute information. We will get back to you as soon as possible.',  # message
                    settings.EMAIL_HOST_USER,  # sender email
                    [email],  # receiver email
                    fail_silently=False,
                    html_message=user_html_message  # HTML message
                )
                
                
                
            # Displaying success message if emails are sent successfully
                messages.success(request, 'Contact form has been successfully sent.')
            except Exception as e:
                # Handling exceptions if email sending fails
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            # Displaying error message if the form is not valid
            messages.error(request, 'Fill out the form completely.')

    else:
        form = DisputeForm()

    return render(request, 'landing_pages/dispute.html', {'form': form})



def terms(request):
    
    return render(request,'landing_pages/terms.html')
def blog(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'landing_pages/blog.html', {'posts': posts,'page_obj':page_obj})


def post(request, pk):
    posts = Post.objects.get(id=pk)
    return render(request, 'landing_pages/posts.html', {'posts': posts})











    