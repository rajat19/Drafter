import os


class DatabaseConfigs:
    def get_config(self):
        db_type = os.environ.get("DB_TYPE") or 'sqlite'
        if db_type == 'pgsql':
            return self.__pgsql_config()
        if db_type == 'mysql':
            return self.__mysql_config()
        if db_type == 'sqlite':
            return self.__sqlite_config()
        if db_type == 'mongo':
            return self.__mongo_config()

    @staticmethod
    def __pgsql_config():
        return {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get("DB_NAME"),
            'USER': os.environ.get("DB_USER"),
            'PASSWORD': os.environ.get("DB_PASSWORD"),
            'HOST': os.environ.get("DB_HOST"),
            'PORT': os.environ.get("DB_PORT"),
        }

    @staticmethod
    def __sqlite_config():
        return {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.environ.get("DB_NAME"),
        }

    @staticmethod
    def __mysql_config():
        return {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get("DB_NAME"),
            'USER': os.environ.get("DB_USER"),
            'PASSWORD': os.environ.get("DB_PASSWORD"),
            'HOST': os.environ.get("DB_HOST"),
            'PORT': os.environ.get("DB_PORT"),
        }

    @staticmethod
    def __mongo_config():
        return {
            'ENGINE': 'djongo',
            'NAME': os.environ.get("DB_NAME"),
            'USER': os.environ.get("DB_USER"),
            'PASSWORD': os.environ.get("DB_PASSWORD"),
            'HOST': os.environ.get("DB_HOST"),
            'PORT': os.environ.get("DB_PORT"),
        }
