from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

INSTALLED_APPS = [
    'orchidea.apps.OrchideaConfig',  # Ensure the app is listed
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',  # Set to 'INFO' or 'ERROR' in production
        },
        'orchidea': {  # Custom logger for your app
            'handlers': ['console'],
            'level': 'DEBUG',  # Ensure this is set to DEBUG
            'propagate': False,  # Prevent duplicate logs
        },
    },
}

MIDDLEWARE = [
    # ...existing code...
    'django.middleware.csrf.CsrfViewMiddleware',  # Ensure this middleware is enabled
    # ...existing code...
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'orchidea/templates'],  # Ensure this points to the correct templates directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "orchidea/static",  # Ensure this points to the correct static directory
]

# Add SVG to recognized file types
import mimetypes
mimetypes.add_type("image/svg+xml", ".svg", True)

import os

FIXTURE_DIRS = [
    BASE_DIR / 'orchidea/fixtures',  # Ensure this points to the correct directory
]