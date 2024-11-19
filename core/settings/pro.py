from .base import *
import logging.config

DEBUG = False

ALLOWED_HOSTS = [
    'rahimagha.ir',
    'www.rahimagha.ir',
     server_ip,     
    'localhost'
    ]

CSRF_TRUSTED_ORIGINS = [
    'https://*.rahimagha.ir',    
    'https://atmancenter.org'
]
CORS_ALLOWED_ORIGINS = [    
    'https://atmancenter.org'
]


SERVER_EMAIL = 'noreply@rahimagha.ir'



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'rotating_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'django_errors.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 10,  # Keep 10 backup files
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'django_debug.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 10,  # Keep 10 backup files
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['rotating_file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'videos': {  # Replace 'myapp' with your actual app name
            'handlers': ['debug_file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
