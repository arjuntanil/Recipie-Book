"""
Absolute direct launcher for Recipe Book - no imports required
"""
import os
import sys
import subprocess

def run_command(command):
    """Run a command and return True if successful"""
    print(f"Running: {command}")
    try:
        process = subprocess.Popen(command, shell=True)
        process.wait()
        return process.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    # Get Python executable
    python = sys.executable
    print(f"Using Python: {python}")
    
    # Install Django globally - this is a brute force approach but will work
    print("\nInstalling Django globally...")
    run_command(f'"{python}" -m pip install --force-reinstall django==5.0.2')
    run_command(f'"{python}" -m pip install --force-reinstall psycopg2-binary==2.9.10 Pillow==11.0.0 django-crispy-forms==2.3 crispy-bootstrap4==2024.10')
    
    # Run server directly
    print("\nRunning Django server directly...\n")
    
    # Set up environment
    os.environ['DJANGO_SETTINGS_MODULE'] = 'recipe_book.settings'
    
    # Change to script directory to make sure we're in the project root
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run migrate
    print("Running migrations...")
    run_command(f'"{python}" manage.py migrate')
    
    # Run server directly
    print("\nStarting server...")
    run_command(f'"{python}" manage.py runserver')

if __name__ == "__main__":
    main() 