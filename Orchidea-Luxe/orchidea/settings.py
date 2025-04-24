DEBUG = True

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

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Ensure this points to the correct static directory
]

# Add SVG to recognized file types
import mimetypes
mimetypes.add_type("image/svg+xml", ".svg", True)