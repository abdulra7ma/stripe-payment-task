from os.path import join

from decouple import config

from .common import *

# ##### DEBUG CONFIGURATION ###############################
DEBUG = config("DEBUG", default=False)

# allow all hosts during development
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# ##### DATABASE CONFIGURATION ############################
DATABASES = {
    "default": {
        "ENGINE": config(
            "SQL_ENGINE", default="django.db.backends.sqlite3", cast=str
        ),
        "NAME": config(
            "SQL_DATABASE",
            default=join(PROJECT_ROOT, "run", "db.sqlite3"),
            cast=str,
        ),
        "USER": config("SQL_USER", default="user", cast=str),
        "PASSWORD": config("SQL_PASSWORD", default="password", cast=str),
        "HOST": config("SQL_HOST", default="localhost", cast=str),
        "PORT": config("SQL_PORT", default="5432", cast=str),
    }
}


# ##### APPLICATION CONFIGURATION #########################
INSTALLED_APPS = DEFAULT_APPS

APPEND_SLASH = False

SITE_ID = 1
