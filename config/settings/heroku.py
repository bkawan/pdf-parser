import os

DEBUG = True
import dj_database_url

from .base import DATABASES, MIDDLEWARE, BASE_DIR

ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']
# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
db_from_env = dj_database_url.config(conn_max_age=500)

DATABASES['default'].update(db_from_env)

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',

]
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
ADMIN_SITE_HEADER = 'PDF Parser Administration'
ADMIN_SITE_TITLE = 'PDF Parser Administration'
ADMIN_SITE_INDEX_TITLE = 'Welcome to PDF parser'