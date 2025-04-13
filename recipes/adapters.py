from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialApp
from django.core.exceptions import MultipleObjectsReturned

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter to handle potential duplicate SocialApp entries
    """
    
    def get_app(self, request, provider, client_id=None):
        """
        Override to handle potential duplicate SocialApp entries
        """
        try:
            # Try the standard way first
            return super().get_app(request, provider, client_id=client_id)
        except MultipleObjectsReturned:
            # If we get multiple objects, use the first one
            app_query = SocialApp.objects.filter(provider=provider)
            if client_id:
                app_query = app_query.filter(client_id=client_id)
            app = app_query.first()
            if app:
                return app
            # If no app is found, let the original exception propagate
            raise 