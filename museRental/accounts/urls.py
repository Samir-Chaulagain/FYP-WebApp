
from django.urls import path


from . import views

app_name = "accounts"
urlpatterns = [
    path('customer/register/', views.customer_registration, name='customer_registration'),
    path('lessor/register/', views.lessor_registration, name='lessor_registration'),
    path('login/', views.user_logIn, name='login'),
    path('logout/', views.user_logOut, name='logout'),
    path('customer/edit/<int:id>/', views.customer_edit_profile, name='customer-edit-profile'),

    path('lessor/edit/<int:id>/', views.lessor_edit_profile, name='lessor-edit-profile'),
    # path('reset/',views.resetPassword,name='reset_pass'),
    # path('changepassword/',views.changePassword,name='change_pass'),
    
    
]


