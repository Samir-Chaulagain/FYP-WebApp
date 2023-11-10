
from django.urls import path

from accounts.forms import CustomerLoginForm,lessorLoginForm
from . import views
from django.contrib.auth import views as auth_views
app_name = "accounts"
urlpatterns = [


     path('customer_register/', views.customer_registration, name='customer_registration'),
    path('lessor_register/', views.lessor_registration, name='lessor_registration'),
    path('customer_login/', auth_views.LoginView.as_view(template_name='accounts/customer-login.html', authentication_form=CustomerLoginForm), name='customer_login'),   
    path('lessor_login/', auth_views.LoginView.as_view(template_name='accounts/lessor-login.html', authentication_form=lessorLoginForm), name='lessor_login'),   
    path('customer_logout/',views.customer_logOut,name='customer_logout'),
    path('lessor_logout/',views.lessor_logOut,name='lessor_logout'),

    # path('reset/',views.resetPassword,name='reset_pass'),
    # path('changepassword/',views.changePassword,name='change_pass'),
    
    
]


