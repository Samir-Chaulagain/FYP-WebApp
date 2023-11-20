
from django.urls import path
from . import views

app_name = "explore"
urlpatterns = [

    path('items/', views.items, name='items'),
    path('items/new/', views.add_item, name='add_item'),
    path('items/<int:id>/', views.showdetails, name='details'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/lessor/item/<int:id>/customers/', views.all_Customers_view, name='customers'),
    path('dashboard/lessor/item/edit/<int:id>', views.item_edit_view, name='edit-item'),
    path('dashboard/lessor/customer/<int:id>/', views.Customer_details_view, name='customer-details'),
    path('dashboard/lessor/close/<int:id>/', views.make_complete_item_view, name='complete'),
    path('dashboard/lessor/delete/<int:id>/', views.delete_item_view, name='delete'),
    path('dashboard/customer/delete-bookmark/<int:id>/', views.delete_save_view, name='delete-bookmark'),
    # path('items/<int:pk>/', views.showdetails, name='details'),
    # path('items/new/', views.upload_items, name='new'),
    # path('items/<int:pk>/delete/', views.delete, name='delete'),
    # path('items/<int:pk>/edit/', views.edit, name='edit'),
   
    
    
]


