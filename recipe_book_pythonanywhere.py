import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/recipe_book'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'recipe_book.settings_prod'
os.environ['PYTHONPATH'] = path

# Import and set up Django's WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 