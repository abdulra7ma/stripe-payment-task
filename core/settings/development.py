# Python imports
from datetime import datetime
from os.path import join

# external imports
from decouple import config

# app imports
from core.swagger.settings import *

# app imports
from .common import *
from .drf import *

# uncomment the following line to include i18n
# from .i18n import *

# ##### DEBUG CONFIGURATION ###############################
DEBUG = config("DEBUG", default=False, cast=bool)

# allow all hosts during development
ALLOWED_HOSTS = ["*"]

# adjust the minimal login
# LOGIN_URL = "core_login"
# LOGIN_REDIRECT_URL = "/"
# LOGOUT_REDIRECT_URL = "core_login"


# ##### DATABASE CONFIGURATION ############################
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": join(PROJECT_ROOT, "run", "dev.sqlite3"),
    }
}

# ##### APPLICATION CONFIGURATION #########################

INSTALLED_APPS = DEFAULT_APPS

AUTH_USER_MODEL = "user.User"


# ##### CORS CONFIGURATION ############################
# CORS_ORIGIN_ALLOW_ALL = False
# CORS_ORIGIN_WHITELIST = ("http://localhost:3000",)


# #####  CELERY CONFIGURATION############################
# CELERY_BROKER_URL = "redis://localhost:6379"
# CELERY_RESULT_BACKEND = "redis://localhost:6379"
# CELERY_ACCEPT_CONTENT = ["application/json", "pickle"]
# CELERY_TASK_SERIALIZER = "json"
# CELERY_RESULT_SERIALIZER = "json"
# CELERY_TIMEZONE = "Asia/Bishkek"
# CELERY_IMPORTS = ("apps.flight.workers.tasks",)


# #####  CELERY BEAT CONFIGURATION############################
# CELERY_BEAT_SCHEDULE = {
#     "delete_flight_ids": {
#         "task": "delete_flight_ids",
#         "schedule": datetime.timedelta(seconds=30),
#         "options": {"expires": 5 * 60},
#     }
# }


# #####  DJANGO LOGGING CONFIGURATION############################
# LOGGING = {
#     "version": 1,
#     "filters": {
#         "require_debug_true": {
#             "()": "django.utils.log.RequireDebugTrue",
#         }
#     },
#     "handlers": {
#         "console": {
#             "level": "DEBUG",
#             "filters": ["require_debug_true"],
#             "class": "logging.StreamHandler",
#         },
#         "file": {
#             "level": "DEBUG",
#             "class": "logging.FileHandler",
#             "filename": f"{PROJECT_ROOT}/logs/django/debug.log",
#         },
#     },
#     "loggers": {
#         "django.db.backends": {
#             "level": "DEBUG",
#             "handlers": ["console"],
#             'formatter': 'verbose'
#         }
#     },
#     "formatters": {
#         "verbose": {
#             "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
#             "style": "{",
#         },
#         "simple": {
#             "format": "{levelname} {message}",
#             "style": "{",
#         },
#     },
# }
