"""
Script to check Django installation and run the server
"""

import subprocess
import sys
import os

def install_django():
    """Install Django and dependencies"""
    print("Installing Django...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "django==5.0.2"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary==2.9.10"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow==11.0.0"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "django-crispy-forms==2.3"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "crispy-bootstrap4==2024.10"])

def check_django():
    """Check if Django is installed"""
    try:
        import django
        print(f"Django {django.get_version()} is installed")
        return True
    except ImportError:
        print("Django is not installed")
        return False

def run_server():
    """Run the Django development server"""
    print("Starting Django development server...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_book.settings')
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(["manage.py", "runserver"])
    except ImportError:
        print("Failed to import Django modules. Make sure Django is properly installed.")
        return False
    return True

if __name__ == "__main__":
    if not check_django():
        print("Django not found. Installing Django...")
        install_django()
        
    if check_django():
        run_server()
    else:
        print("Failed to install Django. Please install it manually with: pip install django==5.0.2")
        input("Press Enter to exit...") 