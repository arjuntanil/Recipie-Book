from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Profile

class Command(BaseCommand):
    help = 'Creates profiles for users that do not have one'

    def handle(self, *args, **options):
        users_without_profile = []
        for user in User.objects.all():
            try:
                # Check if profile exists
                profile = user.profile
            except Profile.DoesNotExist:
                # Create a profile if it does not exist
                users_without_profile.append(user)
                Profile.objects.create(user=user)
        
        if users_without_profile:
            self.stdout.write(self.style.SUCCESS(f'Created profiles for {len(users_without_profile)} users: {", ".join([user.username for user in users_without_profile])}'))
        else:
            self.stdout.write(self.style.SUCCESS('All users already have profiles')) 