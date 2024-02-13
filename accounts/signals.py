# signals.py
from datetime import timezone
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UserLoginHistory

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    UserLoginHistory.objects.create(user=user)

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    last_login_history = UserLoginHistory.objects.filter(user=user).order_by('-login_time').first()
    if last_login_history:
        last_login_history.logout_time = timezone.now()
        last_login_history.save()
