from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.shortcuts import redirect

@receiver(user_signed_up)
def redirect_new_users(sender, request, user, **kwargs):
    request.session['new_google_user'] = True