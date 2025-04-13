"""
Script to fix Python path issues and create a launcher
"""

import sys
import os
import site
import subprocess
import platform

def analyze_environment():
    """Analyze the Python environment and paths"""
    print("=== Python Environment Analysis ===")
    print(f"Python Version: {platform.python_version()}")
    print(f"Python Executable: {sys.executable}")
    print(f"Python Path: {sys.path}")
    
    print("\n=== Site Packages Directories ===")
    for site_dir in site.getsitepackages():
        print(f"- {site_dir}")
    
    print("\n=== Environment Variables ===")
    python_path = os.environ.get('PYTHONPATH', 'Not set')
    print(f"PYTHONPATH: {python_path}")
    
    print("\n=== Checking Django Installation ===")
    try:
        django_path = None
        try:
            import django
            django_path = os.path.dirname(os.path.dirname(django.__file__))
            print(f"Django is installed at: {django_path}")
            print(f"Django version: {django.get_version()}")
        except ImportError:
            print("Django is not installed or not in Python path")
            
        # Check for Django in site-packages
        for site_dir in site.getsitepackages():
            if os.path.exists(os.path.join(site_dir, 'django')):
                print(f"Django found in site-packages: {os.path.join(site_dir, 'django')}")
            
    except Exception as e:
        print(f"Error checking Django: {e}")
        
def create_launcher():
    """Create a launcher script that sets the correct PYTHONPATH"""
    # Find all site-packages directories
    site_dirs = site.getsitepackages()
    
    # Create a launcher script
    with open("launch.bat", "w") as f:
        f.write("@echo off\n")
        f.write("echo Setting up Python environment...\n")
        
        # Set PYTHONPATH to include all site-packages directories
        f.write("set PYTHONPATH=")
        for site_dir in site_dirs:
            f.write(f"{site_dir};")
        f.write("\n")
        
        # Add current directory to PYTHONPATH
        f.write(f"set PYTHONPATH=%PYTHONPATH%;{os.getcwd()}\n")
        
        # Run Django server
        f.write("echo Starting Django server...\n")
        f.write(f"{sys.executable} manage.py runserver\n")
        f.write("pause\n")
    
    print("\n=== Launch Script Created ===")
    print("A launch.bat script has been created to fix path issues.")
    print("Run it with the command: launch.bat")
    
def install_django_clean():
    """Perform a clean installation of Django"""
    print("\n=== Installing Django with Correct Paths ===")
    
    try:
        # First uninstall Django if present
        subprocess.call([sys.executable, "-m", "pip", "uninstall", "-y", "django"])
        
        # Install Django
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "django==5.0.2"])
        
        # Install other dependencies
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade",
            "psycopg2-binary==2.9.10", "Pillow==11.0.0", 
            "django-crispy-forms==2.3", "crispy-bootstrap4==2024.10"
        ])
        
        print("Django and dependencies installed successfully")
    except Exception as e:
        print(f"Error during installation: {e}")

def main():
    """Main function to analyze and fix Python path issues"""
    print("Python Path Fixer Utility")
    print("========================")
    
    # Analyze the current environment
    analyze_environment()
    
    # Perform a clean installation of Django
    install_django_clean()
    
    # Create a launcher script
    create_launcher()
    
    print("\nAll tasks completed. Run the launch.bat script to start the server.")
    
if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...") 