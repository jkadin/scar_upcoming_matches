from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

print("Signals is running!")


@receiver(user_logged_in)
def after_login(sender, request, user, **kwargs):
    print(f"User {user.username} has logged in!")
