from .base import *


if DEBUG:
    # Use insert() to place it in a specific position, often after CommonMiddleware
    # Or use append() to add it to the end. Appending is simpler.
    MIDDLEWARE.append('tools.middleware.QueryCountDebugMiddleware')