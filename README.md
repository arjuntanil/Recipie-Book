# Recipe Book

A full-featured web application for managing and sharing recipes, built with Django and modern web technologies.

## Quick Start Guide (From ZIP File)

1. **Extract the ZIP File**
   - Extract the "Recipe-Book.zip" to your desired location
   - The extracted folder should be named "Recipe-Book"

2. **Install Python**
   - Download and install Python 3.x from [Python's official website](https://www.python.org/downloads/)
   - During installation, make sure to check "Add Python to PATH"
   - Verify installation by opening command prompt and typing:
     ```bash
     python --version
     ```

3. **Setup Virtual Environment**
   ```bash
   # Navigate to the extracted project folder
   cd "path/to/Recipe-Book"

   # Create virtual environment
   python -m venv recipe_book

   # Activate virtual environment
   # On Windows:
   recipe_book\Scripts\activate
   # On Unix or MacOS:
   source recipe_book/bin/activate
   ```

4. **Install Required Packages**
   ```bash
   # Make sure you're in the project root directory
   pip install -r requirements.txt
   ```

5. **Database Setup**
   ```bash
   # Apply migrations
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Website**
   - Open your web browser
   - Go to: `http://127.0.0.1:8000/`
   - Admin interface: `http://127.0.0.1:8000/admin/`
   - Admin login credentials:
     - Username: recipie
     - Password: recipie

## Troubleshooting Common Issues

1. **"Python is not recognized as an internal or external command"**
   - Solution: Reinstall Python and ensure "Add Python to PATH" is checked
   - Or manually add Python to system PATH

2. **"No module named 'django'"**
   ```bash
   # Make sure virtual environment is activated
   # Then reinstall Django
   pip install django==4.2.7
   ```

3. **Database Errors**
   ```bash
   # If you get database errors, try:
   python manage.py migrate --run-syncdb
   ```

4. **Static Files Not Loading**
   ```bash
   # Collect static files
   python manage.py collectstatic --noinput
   ```

5. **Port Already in Use**
   ```bash
   # Try running on a different port
   python manage.py runserver 8080
   ```

## Technologies Used

- **Frontend**:
  - HTML5
  - CSS3 (with Bootstrap 5)
  - JavaScript (ES6+)
  - Font Awesome Icons
  
- **Backend**:
  - Python 3.x
  - Django Web Framework
  - SQLite3 Database
  
- **Authentication**:
  - Django Authentication System
  - Google OAuth Integration

## Features

- User Authentication (Register, Login, Logout)
- Social Authentication (Google)
- Recipe Management (Create, Read, Update, Delete)
- Recipe Categories and Tags
- Recipe Search and Filtering
- User Profiles
- Recipe Ratings and Reviews
- Responsive Design
- Image Upload and Management
- Save Favorite Recipes

## Project Structure

```
RECIPE BOOK/
│
├── recipe_book/                 # Main project directory
│   ├── Scripts/                 # Virtual environment scripts
│   │   ├── activate            # Virtual environment activation script
│   │   └── ...
│   ├── __init__.py
│   ├── settings.py             # Project settings
│   ├── urls.py                 # Main URL configuration
│   └── wsgi.py                 # WSGI configuration
│
├── recipes/                     # Main application directory
│   ├── templates/
│   │   └── recipes/            # Recipe-related templates
│   │       ├── base.html       # Base template
│   │       ├── home.html       # Homepage template
│   │       ├── login.html      # Login page
│   │       ├── register.html   # Registration page
│   │       ├── profile.html    # User profile page
│   │       └── ...
│   │
│   ├── static/                 # Static files (CSS, JS, Images)
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   ├── models.py              # Database models
│   ├── views.py               # View functions
│   ├── urls.py               # URL patterns
│   └── forms.py              # Form definitions
│
└── static/                    # Project-wide static files
    ├── css/
    ├── js/
    └── images/
```

## Required Packages

```
asgiref==3.7.2
certifi==2023.11.17
cffi==1.16.0
charset-normalizer==3.3.2
cryptography==41.0.5
defusedxml==0.7.1
Django==4.2.7
django-allauth==0.58.2
idna==3.4
oauthlib==3.2.2
Pillow==10.1.0
pycparser==2.21
PyJWT==2.8.0
python3-openid==3.2.0
requests==2.31.0
requests-oauthlib==1.3.1
sqlparse==0.4.4
typing_extensions==4.8.0
tzdata==2023.3
urllib3==2.1.0
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd recipe-book
   ```

2. **Set Up Virtual Environment**
   ```bash
   # Navigate to project folder
   cd "RECIPE BOOK"

   # Activate virtual environment
   # On Windows:
   recipe_book\Scripts\activate
   # On Unix or MacOS:
   source recipe_book/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser (Admin)**
   ```bash
   python manage.py createsuperuser already created   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Open web browser and go to: `http://127.0.0.1:8000/`
   - Admin interface: `http://127.0.0.1:8000/admin/`
   - Admin username : recipie
   - Admin password : recipie

## Additional Configuration

### Google OAuth Setup
1. Create a project in Google Cloud Console
2. Enable Google+ API
3. Configure OAuth consent screen
4. Create OAuth 2.0 credentials
5. Add credentials to `settings.py`

### Static Files
- Collect static files:
  ```bash
  python manage.py collectstatic
  ```

## Usage

1. **User Registration**
   - Register using email/password
   - Or use Google Sign-in

2. **Creating Recipes**
   - Click "Add Recipe"
   - Fill in recipe details
   - Upload images
   - Add ingredients and instructions
   - Select category and tags

3. **Managing Recipes**
   - View all recipes
   - Edit your recipes
   - Delete recipes
   - Save favorite recipes

4. **Profile Management**
   - Update profile information
   - Change password
   - View saved recipes


## Acknowledgments

- Bootstrap for the responsive design framework
- Font Awesome for icons
- Django community for the excellent documentation
- All contributors who have helped with the project

 
=======
# Recipie-Book

