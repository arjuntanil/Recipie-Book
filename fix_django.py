"""
Script to fix Django installation
"""

import sys
import subprocess
import os

def main():
    print("Fixing Django installation...")
    
    # Get the Python executable that's currently running this script
    python_executable = sys.executable
    print(f"Using Python executable: {python_executable}")
    
    # Install Django directly using the current Python
    try:
        print("Installing Django...")
        subprocess.check_call([python_executable, "-m", "pip", "install", "django==5.0.2"])
        print("Installing other dependencies...")
        subprocess.check_call([python_executable, "-m", "pip", "install", "psycopg2-binary==2.9.10", "Pillow==11.0.0", "django-crispy-forms==2.3", "crispy-bootstrap4==2024.10"])
        
        # Verify Django is installed
        try:
            import django
            print(f"Success! Django {django.get_version()} is now installed.")
            print("\nYou can now run the server with: python manage.py runserver")
        except ImportError:
            print("Error: Django still can't be imported after installation.")
            print("Try running: pip install django==5.0.2 --force-reinstall")
    except Exception as e:
        print(f"Error during installation: {e}")
        print("Try installing Django manually with: pip install django==5.0.2")

if __name__ == "__main__":
    main()
    input("Press Enter to exit...") 