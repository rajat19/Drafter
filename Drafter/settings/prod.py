from .base import *
import dj_database_url

DEBUG = os.environ.get('DEBUG') or False

ALLOWED_HOSTS.append('draft-machine.herokuapp.com')

if 'USE_LOCAL_DB' in os.environ and os.environ.get('USE_LOCAL_DB') == True:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': os.environ.get("DB_NAME"),
			'USER': os.environ.get("DB_USER"),
			'PASSWORD': os.environ.get("DB_PASSWORD"),
			'HOST': os.environ.get("DB_HOST"),
			'PORT': os.environ.get("DB_PORT"),
		}
	}
else:
	DATABASES['default'] = dj_database_url.config()

MIDDLEWARE_CLASSES.append('whitenoise.middleware.WhiteNoiseMiddleware')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'