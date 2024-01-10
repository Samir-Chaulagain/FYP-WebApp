
from django.urls import path
from . import views
app_name = "event"

urlpatterns = [
     path('event/', views.event, name='event'),
     path('event/<int:pk>/', views.showdetails, name='event-details'),
     path('dashboard/delete-saved/<int:pk>/', views.delete_savedevent_view, name='delete-saved-event'),
     path('saved-event/<int:pk>/', views.event_saved_view, name='saved-event'),
     path('book_event<int:pk>/', views.event_view, name='book-event'),
     path('khalti-payment', views.payment, name='khalti-payment'),
     ]


