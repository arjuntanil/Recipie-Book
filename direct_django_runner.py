"""
Ultra-direct Django runner that bypasses manage.py entirely
"""
import sys
import os
import subprocess

print("RECIPE BOOK ULTRA DIRECT LAUNCHER")
print("=================================")

# Install Django directly
python = sys.executable
print(f"Using Python: {python}")

# Force install Django
print("\nInstalling Django directly...")
subprocess.call([python, "-m", "pip", "install", "--force-reinstall", "django==5.0.2"])
subprocess.call([python, "-m", "pip", "install", "--force-reinstall", 
                "psycopg2-binary==2.9.10", "Pillow==11.0.0", 
                "django-crispy-forms==2.3", "crispy-bootstrap4==2024.10"])

# Set up environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recipe_book.settings")

# Change to script directory to ensure we're in the project root
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Add current directory to Python path
sys.path.insert(0, os.getcwd())

# Set up Django
print("\nSetting up Django...")
try:
    import django
    django.setup()
    print(f"Django {django.get_version()} is set up")
    
    # Run migrations directly
    print("\nRunning migrations...")
    from django.core.management import call_command
    call_command('migrate')
    
    # Run the server directly
    print("\nStarting server at http://127.0.0.1:8000/")
    call_command('runserver')
    
except Exception as e:
    print(f"Error: {e}")
    print("\nTrying backup method...")
    
    # Backup method: use subprocess to run manage.py
    print("Running through manage.py...")
    subprocess.call([python, "manage.py", "runserver"])
    
input("\nPress Enter to exit...") 