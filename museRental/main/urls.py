from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    
    path("blog/", views.blog, name="blog"),
    path("contact/", views.contact, name="contact"),
    path('post/<str:pk>', views.post, name='post'), 
    path('items/', views.items, name='items'),
    path('items/new/', views.new, name='new'),
    path('items/<int:pk>/', views.detail, name='detail'),
    path('items/<int:pk>/delete/', views.delete, name='delete'),
    path('items/<int:pk>/edit/', views.edit, name='edit'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)