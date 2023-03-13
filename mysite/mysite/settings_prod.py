"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from mysite.settings_base import *

print('In prod............')

DEBUG = False

# Note: Replace 'supersecure.codes' with your domain
STATIC_ROOT = "/var/www/asuperdomain.com/static"
STATICFILES_DIRS = [BASE_DIR / "embedding/static"]

SECURE_HSTS_SECONDS = 60  # Unit is seconds; *USE A SMALL VALUE FOR TESTING!*
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")