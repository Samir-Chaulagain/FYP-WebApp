
from django.urls import path
from . import views

app_name = "explore"
urlpatterns = [

     path('items/', views.items, name='items'),
    path('items/<int:pk>/', views.showdetails, name='details'),
    # path('items/new/', views.upload_items, name='new'),
    # path('items/<int:pk>/delete/', views.delete, name='delete'),
    # path('items/<int:pk>/edit/', views.edit, name='edit'),
   
    
    
]


