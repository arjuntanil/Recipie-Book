from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.conf import settings
import os
import shutil
from django.core.files import File

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        
        # Set a default profile picture
        default_img_path = os.path.join(settings.MEDIA_ROOT, 'default.jpg')
        if os.path.exists(default_img_path):
            with open(default_img_path, 'rb') as f:
                profile.profile_picture.save('default.jpg', File(f), save=True)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # Check if profile exists, if not create one
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance) 