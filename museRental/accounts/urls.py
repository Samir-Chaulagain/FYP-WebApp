
from django.urls import path
from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, activate_user
from . import views

app_name = "accounts"
urlpatterns = [
    path('customer/register/', views.customer_registration, name='customer_registration'),
    path('lessor/register/', views.lessor_registration, name='lessor_registration'),
    path('login/', views.user_logIn, name='login'),
    path('logout/', views.user_logOut, name='logout'),
    path('profile/customer-edit/<int:id>/', views.customer_edit_profile, name='customer-edit-profile'),
    path('profile/lessor-edit/<int:id>/', views.lessor_edit_profile, name='lessor-edit-profile'),
    # path('change_password/', views.change_password, name='change_password'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', activate_user, name='activate'),
    
]


