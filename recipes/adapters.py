from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
from allauth.utils import get_user_model
from django.conf import settings

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Handle cases where a user's email already exists.
        If a user with this email exists, connect the social account to it.
        """
        # Get the email from the social account
        email = sociallogin.account.extra_data.get('email')
        if email:
            # Check if any user exists with this email
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                # If we found a user, connect the social account to it
                if not sociallogin.is_existing:
                    sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass
        
        return super().pre_social_login(request, sociallogin)

    def populate_user(self, request, sociallogin, data):
        """
        Populate user information from social login.
        """
        user = super().populate_user(request, sociallogin, data)
        if not user.email:
            user.email = data.get('email', '')
        return user 