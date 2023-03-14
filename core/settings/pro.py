from .base import *


DEBUG = False

ALLOWED_HOSTS = [
    'rahimagha.ir',
    'www.rahimagha.ir',
     server_ip,     
    'localhost'
    ]

CSRF_TRUSTED_ORIGINS = ['https://*.rahimagha.ir']

SERVER_EMAIL = 'noreply@rahimagha.ir'
