from .base import *
import dj_database_url

DEBUG = os.environ.get('DEBUG') or False

ALLOWED_HOSTS.append('draft-machine.herokuapp.com')

if 'USE_LOCAL_DB' not in os.environ or os.environ.get('USE_LOCAL_DB') is False:
	DATABASES['default'] = dj_database_url.config()

MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
