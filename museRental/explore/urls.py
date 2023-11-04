
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

     path('items/', views.items, name='items'),
    path('items/new/', views.new, name='new'),
    path('items/<int:pk>/', views.detail, name='detail'),
    path('items/<int:pk>/delete/', views.delete, name='delete'),
    path('items/<int:pk>/edit/', views.edit, name='edit'),
   
    
    
]


