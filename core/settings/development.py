from datetime import datetime
from os.path import join

from .common import *
from .environment import env

# ##### DEBUG CONFIGURATION ###############################
DEBUG = env("DEBUG", default=False)

# allow all hosts during development
ALLOWED_HOSTS = ["*"]


# ##### DATABASE CONFIGURATION ############################
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": join(PROJECT_ROOT, "run", "dev.sqlite3"),
#     }
# }

DATABASES = {
    "default": env.db("CORE_DATABASE_URL", default="psql://postgres:schoolsite_db_password_1@database:5432/schoolsite_db")
}

# ##### APPLICATION CONFIGURATION #########################

INSTALLED_APPS = DEFAULT_APPS


AUTH_USER_MODEL = "school.Teacher"

LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/school/"
LOGOUT_REDIRECT_URL = "/auth/login/"

SENDGRID_API_KEY = env("SENDGRID_API_KEY", default="API_KEY")
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
