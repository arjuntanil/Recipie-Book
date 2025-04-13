import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_book.settings')
django.setup()

# Create superuser
from django.contrib.auth.models import User

if not User.objects.filter(username='recipie').exists():
    User.objects.create_superuser('recipie', 'recipie@gmail.com', 'recipie')
    print("Superuser 'recipie' created successfully!")
else:
    print("Superuser 'recipie' already exists.") 