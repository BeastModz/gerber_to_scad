"""
Django settings for Railway deployment.

This module imports from base settings and overrides configurations
for production deployment on Railway.
"""

import os
from gts_service.settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allow Railway domains
ALLOWED_HOSTS = [
    '*.railway.app',
    '.railway.app',
    'localhost',
    '127.0.0.1',
]

# Static files configuration for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# OpenSCAD binary location in Docker container
OPENSCAD_BIN = '/usr/bin/openscad'

# Add gunicorn to installed apps
if 'gunicorn' not in INSTALLED_APPS:
    INSTALLED_APPS = INSTALLED_APPS + ['gunicorn']

# CSRF trusted origins for Railway
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
]

# Use environment variable for SECRET_KEY in production
# WARNING: The fallback key below is only for initial deployment convenience.
# For production use, ALWAYS set a unique SECRET_KEY environment variable.
# Generate one using: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    '-7lxck0^d7y#5$fq3ubvtm1*_g%nzd-=ich_1x)^f)8j)hgps+'  # Fallback for initial deployment
)

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
