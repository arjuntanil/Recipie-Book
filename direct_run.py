"""
Direct script to run Django without using manage.py
"""

import sys
import os
import subprocess

# Install Django first
subprocess.call([sys.executable, "-m", "pip", "install", "django==5.0.2"])

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_book.settings')

# Try importing Django
try:
    import django
    django.setup()

    # Import the WSGI application
    from django.core.management.commands.runserver import Command as RunServerCommand
    
    # Run the server directly
    print("Starting Django development server...")
    server = RunServerCommand()
    server.handle(addrport="127.0.0.1:8000", use_ipv6=False, use_reloader=True)
    
except ImportError as e:
    print(f"Error importing Django: {e}")
    print("Try installing Django with: pip install django==5.0.2")
    input("Press Enter to exit...") 