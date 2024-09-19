from .base import *


DEBUG = False

ALLOWED_HOSTS = [
    'rahimagha.ir',
    'www.rahimagha.ir',
     server_ip,     
    'localhost'
    ]

CSRF_TRUSTED_ORIGINS = [
    'https://*.rahimagha.ir',
    'https://computermuseum.ir',
    'https://atmancenter.org'
]
CORS_ALLOWED_ORIGINS = [
    'https://computermuseum.ir',
    'https://atmancenter.org'
]


SERVER_EMAIL = 'noreply@rahimagha.ir'
