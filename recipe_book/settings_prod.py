from .settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pe8ab_7!qv0ta=ce0*u=_@_p951q(^68d$4+!pp%p^whu#-ijh'

# Temporarily enable debug to see the error
DEBUG = True

# Add your PythonAnywhere domain to allowed hosts
ALLOWED_HOSTS = ['arjuntanil24pmc.pythonanywhere.com']

# Database settings - Use SQLite for simplicity
# If you want to use MySQL on PythonAnywhere, you'll need to configure it separately
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files configuration
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Media files configuration
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Security settings
CSRF_COOKIE_SECURE = False  # Changed to False for non-HTTPS
SESSION_COOKIE_SECURE = False  # Changed to False for non-HTTPS
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# CSRF Settings
CSRF_TRUSTED_ORIGINS = ['http://arjuntanil24pmc.pythonanywhere.com']
CSRF_COOKIE_DOMAIN = 'arjuntanil24pmc.pythonanywhere.com'

# Email settings (configure according to your email provider)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development

# Social Auth Settings
SITE_ID = 1

# Update the social account settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# Make sure these are included
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Additional allauth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
SOCIALACCOUNT_AUTO_SIGNUP = True

# Add these settings for debugging OAuth
SOCIALACCOUNT_LOG_LEVEL = 'DEBUG'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'allauth': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
} 