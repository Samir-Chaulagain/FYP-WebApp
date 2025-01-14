
from django.conf import settings
from django.urls import path

from django.conf.urls.static import static
from . import views

app_name = "explore"
urlpatterns = [

    path('items/', views.items, name='items'),
    path('items/<int:id>/', views.showdetails, name='details'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('items/new/', views.add_item, name='add_item'),
    
    path('dashboard/lessor/item/edit/<int:id>', views.item_edit_view, name='edit-item'),
    # path('dashboard/lessor/close/<int:id>/', views.make_complete_item_view, name='complete'),
    path('dashboard/lessor/delete/<int:id>/', views.delete_item, name='delete-item'),
    path('check_availability/<int:id>/', views.CheckAvailability, name='CheckAvailability'),
    path('rent-item/<int:id>/', views.rent_item_view, name='rent-item'),
    path('dashboard/lessor/item/<int:id>/allcustomers/', views.all_Customers_view, name='customers'),
    path('dashboard/lessor/customer/<int:id>/', views.Customer_details_view, name='customer-details'),    
    path('save-item/<int:id>/', views.item_saved_view, name='saved-item'),
    path('delete-saved/<int:id>/', views.delete_save_view, name='delete-saved'),
    path('delete-saved_dashboard/<int:id>/', views.deletesaveditem, name='deletesaveditem_d'),
    path('send-email-after-payment/', views.send_email_after_payment, name='send_email_after_payment'),
    path('update_status/', views.update_status, name='update_status'),
    path('rate/<int:id>/', views.rate_item, name='add-rate'),

   
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
