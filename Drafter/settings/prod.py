from .base import *
from Drafter.databaseConfigs import DatabaseConfigs
import dj_database_url

DEBUG = os.environ.get('DEBUG') or False

ALLOWED_HOSTS.append('draft-machine.herokuapp.com')

if 'USE_LOCAL_DB' in os.environ and os.environ.get('USE_LOCAL_DB') is True:
	DATABASES['default'] = DatabaseConfigs.get_postgresql_config()
else:
	DATABASES['default'] = dj_database_url.config()

MIDDLEWARE_CLASSES.append('whitenoise.middleware.WhiteNoiseMiddleware')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
