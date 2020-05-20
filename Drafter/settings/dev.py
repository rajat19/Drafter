from .base import *

DEBUG = os.environ.get('DEBUG') or True

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
