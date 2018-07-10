DEBUG = True
import dj_database_url

from .base import DATABASES, MIDDLEWARE

ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']
# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
db_from_env = dj_database_url.config(conn_max_age=500)

DATABASES['default'].update(db_from_env)

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',

]
