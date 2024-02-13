
from django.urls import path
from . import views

app_name = "event"

urlpatterns = [
     path('event/', views.event, name='event'),
     path('event/<int:pk>/', views.showdetails, name='event-details'),
     path('saved-event/<int:pk>/', views.event_saved_view, name='saved-event'),
     
     path('delete-saved/<int:pk>/', views.delete_savedevent_d, name='deletesavedevent_d'),

     path('book_event<int:pk>/', views.event_view, name='book-event'),
     path('mark_paid/<int:pk>/', views.mark_paid_view, name='mark-paid'),
     path('delete_event/<int:pk>/', views.delete_booking, name='delete-event'),
     path('edit_booking/<int:pk>/', views.edit_booking, name='edit-booking'),
     
    
     ]


