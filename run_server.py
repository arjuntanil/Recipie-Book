#!/usr/bin/env python
"""
This script runs the Django development server.
It's an alternative to using 'python manage.py runserver'.
"""

import os
import sys
import subprocess

def main():
    # Check if Django is installed
    try:
        import django
        print(f"Django version: {django.get_version()}")
    except ImportError:
        print("Django is not installed. Install it using: pip install django")
        print("Or activate your virtual environment if Django is installed there.")
        sys.exit(1)
    
    # Run the development server
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_book.settings')
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'runserver'])
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 