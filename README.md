# Recipe Book Web Application

A web application for adding, viewing, and searching for recipes. Built with Django, PostgreSQL, HTML, CSS, and JavaScript.

## Features

- **Add Recipes**: Add new recipes with name, description, preparation steps, ingredients, and images
- **View Recipes**: Browse all recipes with details and images
- **Search Functionality**: Search for recipes by name, description, or ingredients
- **Responsive Design**: Works on mobile, tablet, and desktop devices

## Technology Stack

- **Backend**: Django 5.0.2
- **Database**: SQLite (for development)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Image Handling**: Pillow
- **Form Styling**: django-crispy-forms with crispy-bootstrap4

## Installation & Setup

### Virtual Environment Setup (Recommended)

This method properly isolates your project dependencies in a virtual environment:

#### Windows

1. Run the virtual environment setup script:
   ```
   setup_venv.bat
   ```

This script will:
- Create a fresh virtual environment in the 'venv' directory
- Install all dependencies in the isolated environment
- Run database migrations
- Create the default superuser (username: recipie, password: recipie)
- Offer to run the server

After running this script once, in the future you can just:
1. Activate the environment: `venv\Scripts\activate.bat`
2. Run the server: `python manage.py runserver`

#### Unix/Mac

1. Make the setup script executable:
   ```
   chmod +x setup_venv.sh
   ```

2. Run the setup script:
   ```
   ./setup_venv.sh
   ```

After running this script once, in the future you can just:
1. Activate the environment: `source venv/bin/activate`
2. Run the server: `python manage.py runserver`

### Alternative Setup Methods

If the virtual environment setup doesn't work, try one of these alternatives:

#### Option 1: Django Fixer script (Windows)
```
django_fix.bat
```
This sets the PYTHONPATH to fix import issues and runs the server.

#### Option 2: Using the standalone launcher
```
python standalone_launcher.py
```
This will install Django and create a `run_recipe_book.bat` file you can use to start the server.

#### Option 3: Using the path fixer
```
python path_fixer.py
```
This will analyze your Python environment, install Django, and create a `launch.bat` file.

#### Option 4: Using the direct Django installer
```
python install_direct.py
```
This will install Django directly in your site-packages directory.

### Manual Setup

1. Create and activate a virtual environment:
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Unix/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Apply migrations:
   ```
   python manage.py migrate
   ```

4. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```

## Troubleshooting

If you encounter the "No module named 'django'" error:

1. Make sure the virtual environment is activated:
   ```
   # Windows
   venv\Scripts\activate.bat
   
   # Unix/Mac
   source venv/bin/activate
   ```

2. Verify Django is installed in the environment:
   ```
   pip list
   ```

3. If Django is missing, install it:
   ```
   pip install django==5.0.2
   ```

4. If issues persist, try one of the alternative setup methods described above.

## Usage

1. Visit the home page to view all recipes
2. Click on "Add Recipe" to create a new recipe
3. Fill in recipe details, add ingredients, and upload images
4. Use the search box to find recipes by name, ingredients, or description
5. Click on a recipe to view its details, or use the edit/delete options

## Project Structure

- **recipes/**: Main application with models, views, and forms
- **templates/**: HTML templates
- **static/**: Static files (CSS, JS, images)
- **media/**: User-uploaded media files

## License

This project is licensed under the MIT License.

## Solution to the Django Import Error

I've created a special script to fix your Django installation issue and run the server. This approach should work even when the standard methods fail.

### Steps to run your project:

1. **Run the fix_and_run.py script**
   ```
   python fix_and_run.py
   ```

This script will:
1. Force reinstall Django to ensure it's in the correct Python environment
2. Install all necessary dependencies
3. Refresh the Python package paths to make sure Django is found
4. Verify that Django is properly installed
5. Run the database migrations
6. Start the server using `manage.py runserver`

The script includes extensive error handling and will provide helpful messages if something goes wrong.

### What makes this solution different:

1. **Forces a clean reinstall** of Django to fix any path or environment issues
2. **Refreshes the package paths** during runtime to ensure Django is found
3. **Uses the current Python interpreter** that's running the script to install Django
4. **Provides detailed troubleshooting information** if anything fails

This approach addresses the common causes of the "No module named 'django'" error:
- Incorrect virtual environment activation
- Django installed in a different Python environment than the one being used
- Path issues preventing Python from finding the Django package
- Installation conflicts

Once the script runs successfully, you should be able to use the standard `python manage.py runserver` command directly as well.

 