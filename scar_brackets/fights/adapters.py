from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from fights.models import Profile


class MySocialAccountAdapter(DefaultSocialAccountAdapter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def pre_social_login(self, request, sociallogin):
        # Custom logic for handling social logins
        user = User.objects.get(username=sociallogin.user.username)
        profile, created = Profile.objects.get_or_create(user=user)
