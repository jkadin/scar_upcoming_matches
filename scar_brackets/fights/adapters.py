from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from fights.models import Profile
from django.contrib.auth import login


class MySocialAccountAdapter(DefaultSocialAccountAdapter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def pre_social_login(self, request, sociallogin):
        # Custom logic for handling social logins
        try:
            user = User.objects.get(username=sociallogin.user.username)
        except User.DoesNotExist:
            user = User.objects.create(
                username=sociallogin.user.username,
                email=sociallogin.user.email,
                # Set other fields as needed
            )
        # Authenticate and log in the user
        sociallogin.connect(request, user)
        profile, created = Profile.objects.get_or_create(user=user)
