@echo off
echo Django Installation and Path Fixer
echo =================================

REM Get the Python executable
for /f "tokens=*" %%i in ('where python') do set PYTHON_EXE=%%i
echo Using Python executable: %PYTHON_EXE%

REM Install Django
echo.
echo Step 1: Installing Django and dependencies...
%PYTHON_EXE% -m pip install --force-reinstall django==5.0.2
%PYTHON_EXE% -m pip install --force-reinstall psycopg2-binary==2.9.10 Pillow==11.0.0 django-crispy-forms==2.3 crispy-bootstrap4==2024.10

REM Locate the site-packages directory
echo.
echo Step 2: Locating site-packages directory...
for /f "tokens=*" %%i in ('%PYTHON_EXE% -c "import site; print(site.getsitepackages()[0])"') do set SITE_PACKAGES=%%i
echo Site packages directory: %SITE_PACKAGES%

REM Set up the PYTHONPATH to include site-packages
echo.
echo Step 3: Setting up PYTHONPATH...
set PYTHONPATH=%SITE_PACKAGES%;%CD%
echo PYTHONPATH set to: %PYTHONPATH%

REM Verify Django installation
echo.
echo Step 4: Verifying Django installation...
%PYTHON_EXE% -c "import django; print(f'Django {django.get_version()} found at {django.__file__}')"
if %errorlevel% neq 0 (
    echo Error: Django still not found. Manual intervention required.
    pause
    exit /b 1
)

REM Run database migrations
echo.
echo Step 5: Running database migrations...
%PYTHON_EXE% manage.py migrate

REM Create superuser if needed
echo.
echo Step 6: Creating superuser...
%PYTHON_EXE% -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_book.settings'); import django; django.setup(); from django.contrib.auth.models import User; User.objects.filter(username='recipie').exists() or User.objects.create_superuser('recipie', 'recipie@gmail.com', 'recipie'); print('Superuser created/verified')"

REM Run the server
echo.
echo Step 7: Starting Django development server...
echo You can access the application at: http://127.0.0.1:8000/
echo Admin interface available at: http://127.0.0.1:8000/admin/
echo Username: recipie
echo Password: recipie
echo Use Ctrl+C to stop the server
echo.
%PYTHON_EXE% manage.py runserver

pause 