
from django.urls import path
from . import views
app_name = "event"

urlpatterns = [
     path('event/', views.event, name='event'),
     path('book_event<int:pk>/', views.book_event, name='book-event'),
     path('event/<int:pk>/', views.showdetails, name='event-details'),
     path('paypal/<int:pk>', views.paypal, name="paypal"),
     
     ]


