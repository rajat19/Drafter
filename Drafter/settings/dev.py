from .base import *
from Drafter.databaseConfigs import DatabaseConfigs

DATABASES = {
    'default': DatabaseConfigs.get_sqlite_config()
}

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
