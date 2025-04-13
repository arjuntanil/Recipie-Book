"""
Fix Django installation and then run manage.py runserver
"""

import sys
import subprocess
import os
import site

def main():
    print("=======================================")
    print("Django Installation and Server Launcher")
    print("=======================================")
    
    # Get the current Python executable
    python_exe = sys.executable
    print(f"Using Python: {python_exe}")
    
    # Force a clean reinstall of Django in the current Python environment
    print("\nStep 1: Installing Django...")
    try:
        # Force reinstall Django to ensure it's in the correct environment
        subprocess.check_call([python_exe, "-m", "pip", "install", "--force-reinstall", "django==5.0.2"])
        
        # Install other dependencies
        print("\nStep 2: Installing other dependencies...")
        subprocess.check_call([python_exe, "-m", "pip", "install", "psycopg2-binary==2.9.10", 
                               "Pillow==11.0.0", "django-crispy-forms==2.3", 
                               "crispy-bootstrap4==2024.10"])
        
        # Reload site packages to ensure Django is found
        print("\nStep 3: Refreshing package paths...")
        importlib_found = False
        try:
            import importlib
            importlib.invalidate_caches()
            importlib_found = True
        except ImportError:
            pass
            
        # Reload site-packages
        site.main()
        
        # Test Django import
        print("\nStep 4: Verifying Django installation...")
        try:
            import django
            print(f"Django {django.get_version()} successfully installed!")
        except ImportError as e:
            print(f"Error: Failed to import Django after installation: {e}")
            return False
            
        # Run database migrations
        print("\nStep 5: Running migrations...")
        subprocess.call([python_exe, "manage.py", "migrate"])
        
        # Run the server using manage.py
        print("\nStep 6: Starting the development server...")
        print("You can access the application at: http://127.0.0.1:8000/")
        print("Use Ctrl+C to stop the server.")
        subprocess.call([python_exe, "manage.py", "runserver"])
        
        return True
        
    except Exception as e:
        print(f"\nError: {e}")
        return False
        
if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n============================================")
        print("Troubleshooting tips:")
        print("1. Make sure you're running this script with the Python version you want to use")
        print("2. Try manually running: pip install django==5.0.2")
        print("3. Check if your Python environment is properly set up")
        print("============================================")
    
    input("\nPress Enter to exit...") 