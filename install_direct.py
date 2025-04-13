"""
Script to install Django directly where Python can find it
"""

import sys
import subprocess
import os
import importlib.util
import site

# Get Python executable path and site-packages directory
python_exe = sys.executable
site_packages = site.getsitepackages()[0]
print(f"Python executable: {python_exe}")
print(f"Site packages directory: {site_packages}")

# Install Django in the specific site-packages directory
print("\nInstalling Django in the correct site-packages directory...")
try:
    # Uninstall any existing Django first
    subprocess.call([python_exe, "-m", "pip", "uninstall", "-y", "django"])
    
    # Install Django directly
    subprocess.check_call([
        python_exe, "-m", "pip", "install", 
        "--target", site_packages,
        "--no-cache-dir", "--upgrade",
        "django==5.0.2"
    ])
    
    # Also install other requirements
    subprocess.check_call([
        python_exe, "-m", "pip", "install", 
        "--target", site_packages,
        "--no-cache-dir", "--upgrade",
        "psycopg2-binary==2.9.10", "Pillow==11.0.0", 
        "django-crispy-forms==2.3", "crispy-bootstrap4==2024.10"
    ])

    # Update paths
    sys.path.insert(0, site_packages)
    
    # Try to import Django to verify
    spec = importlib.util.find_spec("django")
    if spec:
        print(f"\nSuccess! Django is now installed at: {spec.origin}")
        import django
        print(f"Django version: {django.get_version()}")
        print("\nYou can now run the server with: python manage.py runserver")
    else:
        print("\nError: Django is still not in the Python path after installation")
        
except Exception as e:
    print(f"\nError during installation: {e}")

input("\nPress Enter to exit...") 