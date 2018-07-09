DEBUG = False
import dj_database_url
from .base import DATABASES

ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)