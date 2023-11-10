
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = "accounts"
urlpatterns = [

     path('customer/register/', views.customer_registration, name='customer_registration'),
    path('lessor/register/', views.lessor_registration, name='lessor_registration'),
    # path('profile/edit/<int:id>/', views.customer_edit_profile, name='edit-profile'),
    path('customer_logIn',views.customer_logIn, name='customer_login'),
    path('lessor_login',views.lessor_logIn, name='lessor_login'),
    path('logout/',views.user_logOut,name='logout'),
    # path('reset/',views.resetPassword,name='reset_pass'),
    # path('changepassword/',views.changePassword,name='change_pass'),
    
    
]


