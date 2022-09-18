from os.path import join

from decouple import config

from .common import *

# ##### DEBUG CONFIGURATION ###############################
DEBUG = config("DEBUG", default=False, cast=bool)

# allow all hosts during development
ALLOWED_HOSTS = ["*"]


# ##### DATABASE CONFIGURATION ############################
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DATABASE_NAME", default="postgres", cast=str),
        "USER": config("POSTGRES_DATABASE_USER", default="postgres", cast=str),
        "PASSWORD": config(
            "POSTGRES_DATABASE_PASSWORD", default="password", cast=str
        ),
        "HOST": config("POSTGRES_DATABASE_HOST", default="localhost", cast=str),
        "PORT": config("POSTGRES_DATABASE_PORT", default="5432", cast=str),
    }
}

# ##### APPLICATION CONFIGURATION #########################
INSTALLED_APPS = DEFAULT_APPS


# ##### CORS CONFIGURATION ############################
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ("http://localhost:3000",)
