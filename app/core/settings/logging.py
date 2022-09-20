from .path import PROJECT_ROOT

LOGGING = {
    "version": 1,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": f"{PROJECT_ROOT}/logs/django/debug.log",
        },
    },
    "loggers": {
        "django.db.backends": {
            "level": "DEBUG",
            "handlers": ["console"],
            "formatter": "verbose",
        }
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
}
