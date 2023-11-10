
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = "accounts"
urlpatterns = [

     path('customer/register/', views.customer_registration, name='customer-registration'),
    path('lessor/register/', views.lessor_registration, name='lessor-registration'),
    path('profile/edit/<int:id>/', views.customer_edit_profile, name='edit-profile'),
    path('login/',views.user_logIn, name='login'),
    path('logout/',views.user_logOut,name='logout'),
    # path('reset/',views.resetPassword,name='reset_pass'),
    # path('changepassword/',views.changePassword,name='change_pass'),
    
    
]


