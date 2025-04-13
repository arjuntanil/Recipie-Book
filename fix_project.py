"""
Direct fix for Django import error
"""
import subprocess
import sys
import os

def main():
    print("===== RECIPE BOOK PROJECT REPAIR TOOL =====")
    print("This will fix the 'No module named django' error")
    
    # Use the current Python
    python = sys.executable
    print(f"Using Python: {python}")
    
    # Force reinstall Django and dependencies
    print("\nReinstalling Django directly...")
    try:
        subprocess.check_call([python, "-m", "pip", "install", "--force-reinstall", "django==5.0.2"])
        subprocess.check_call([python, "-m", "pip", "install", "--force-reinstall", 
                              "psycopg2-binary==2.9.10", "Pillow==11.0.0", 
                              "django-crispy-forms==2.3", "crispy-bootstrap4==2024.10"])
        print("Installation successful")
    except Exception as e:
        print(f"Error during installation: {e}")
        return False
    
    # Verify Django installed correctly
    print("\nVerifying Django installation...")
    try:
        # Add current directory to path to ensure the script can find the project
        sys.path.insert(0, os.getcwd())
        
        # Try to import Django
        import django
        print(f"Django {django.get_version()} found at {django.__file__}")
        
        # Create a direct launch script
        print("\nCreating a reliable launch script...")
        with open("run_server.bat", "w") as f:
            f.write("@echo off\n")
            f.write(f"set PYTHONPATH={os.path.dirname(django.__file__)}\\..;%CD%\n")
            f.write(f"\"{python}\" manage.py migrate\n")
            f.write(f"\"{python}\" manage.py runserver\n")
            f.write("pause\n")
            
        print("Launch script created: run_server.bat")
        print("\nProject fixed successfully!")
        print("\nTo run the project, use: run_server.bat")
        
        return True
    except ImportError:
        print("ERROR: Django still not found after installation.")
        print("Let's try a more direct approach...")
        
        # Create a script that sets PYTHONPATH explicitly
        site_packages = os.path.join(os.path.dirname(os.path.dirname(python)), "Lib", "site-packages")
        with open("emergency_run.bat", "w") as f:
            f.write("@echo off\n")
            f.write(f"set PYTHONPATH={site_packages};%CD%\n")
            f.write(f"\"{python}\" -m pip install django==5.0.2\n")
            f.write(f"\"{python}\" manage.py runserver\n")
            f.write("pause\n")
            
        print("\nEmergency launcher created: emergency_run.bat")
        print("Please run this file to start the server")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\nIf you're still having issues, try running the emergency launcher.")
    
    input("\nPress Enter to exit...") 