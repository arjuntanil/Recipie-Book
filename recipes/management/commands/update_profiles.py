from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Profile
from django.conf import settings
import os
from django.core.files import File

class Command(BaseCommand):
    help = 'Updates profile pictures for all users'

    def handle(self, *args, **options):
        default_img_path = os.path.join(settings.MEDIA_ROOT, 'default.jpg')
        
        if not os.path.exists(default_img_path):
            self.stdout.write(self.style.ERROR(f'Default image not found at {default_img_path}'))
            return
            
        # Ensure profile pictures directory exists
        profile_pics_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pics')
        if not os.path.exists(profile_pics_dir):
            os.makedirs(profile_pics_dir)
            self.stdout.write(self.style.SUCCESS(f'Created profile pictures directory at {profile_pics_dir}'))
        
        updated_count = 0
        for user in User.objects.all():
            try:
                # Create profile if doesn't exist
                profile, created = Profile.objects.get_or_create(user=user)
                
                # Check if profile picture is missing or using default with wrong path
                if not profile.profile_picture or not os.path.exists(profile.profile_picture.path):
                    with open(default_img_path, 'rb') as f:
                        profile.profile_picture.save(f'user_{user.id}_default.jpg', File(f), save=True)
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Updated profile picture for {user.username}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error updating profile for {user.username}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'Updated {updated_count} profile pictures')) 