from .base import *  # noqa
from .base import env
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration
import logging

# GENERAL
# ------------------------------------------------------------------------------
PORT = env.str("PORT", "8000")
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="aaI4cw0xJn50UnxZSsTiqEdcYyVdZkkX1vtn5BPa7U8iVM6m8GZFHY3fpwaTWeis",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])
ADMIN_URL = env("DJANGO_ADMIN_URL")

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 1025
EMAIL_PRODUCTION = env.bool("EMAIL_PRODUCTION", default=False)

if EMAIL_PRODUCTION:
    DEFAULT_FROM_EMAIL = env(
        "DJANGO_DEFAULT_FROM_EMAIL",
        default="backend <noreply@example.com>",
    )
    SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
    EMAIL_SUBJECT_PREFIX = env(
        "DJANGO_EMAIL_SUBJECT_PREFIX",
        default="[backend] ",
    )
    EMAIL_HOST = env("DJANGO_EMAIL_HOST", default="")
    EMAIL_PORT = env("DJANGO_EMAIL_PORT", default="")
    EMAIL_HOST_USER = env("DJANGO_EMAIL_HOST_USER", default="")
    EMAIL_HOST_PASSWORD = env("DJANGO_EMAIL_HOST_PASSWORD", default="")
    EMAIL_USE_TLS = env.bool("DJANGO_EMAIL_USE_TLS", default=False)
    EMAIL_USE_SSL = env.bool("DJANGO_EMAIL_USE_SSL", default=False)
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa: F405


# django-silk (if neded)
# ------------------------------------------------------------------------------
# INSTALLED_APPS += ["silk"]  # noqa: F405
# MIDDLEWARE += ["silk.middleware.SilkyMiddleware"]  # noqa: F405

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
# INSTALLED_APPS += ["django_extensions"]  # noqa: F405
# Celery
# ------------------------------------------------------------------------------

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-eager-propagates
CELERY_TASK_EAGER_PROPAGATES = True

# CORS
# https://github.com/adamchainz/django-cors-headers
# ------------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = (
    ["https://" + host for host in ALLOWED_HOSTS]
    + ["http://" + host for host in ALLOWED_HOSTS]
    # + [
    #     "http://127.0.0.1:3019",
    #     "http://localhost:3019",
    # ]
)
CSRF_TRUSTED_ORIGINS = ["https://" + host for host in ALLOWED_HOSTS] + [
    "http://" + host for host in ALLOWED_HOSTS
]
SECURE_CROSS_ORIGIN_OPENER_POLICY = None  # type: ignore
CSRF_COOKIE_DOMAIN = env.str("DOMAIN", default="localhost")
# CORS_ALLOW_ALL_ORIGINS = True
# CSRF_TRUSTED_ORIGINS = [
#     "https://tpl.local",
#     "http://tpl.local",
#     "http://127.0.0.1",
#     "http://127.0.0.1:3018",
#     "http://localhost",
#     "http://localhost:3018",
#     "http://0.0.0.0",
#     "http://0.0.0.0:3018",
# ]

# CORS_ALLOW_METHODS = [
#     "DELETE",
#     "GET",
#     "OPTIONS",
#     "PATCH",
#     "POST",
#     "PUT",
# ]
# CORS_ALLOW_HEADERS = [
#     "accept",
#     "accept-encoding",
#     "authorization",
#     "content-type",
#     "dnt",
#     "origin",
#     "user-agent",
#     "x-csrftoken",
#     "x-requested-with",
#     "content-disposition",
#     "sentry-trace",
#     "baggage",
# ]
# CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_ALLOW_ALL = env.bool("CORS_ORIGIN_ALLOW_ALL", default=True)
# CORS_ORIGIN_WHITELIST = (
#     "https://tpl.local",
#     "http://tpl.local",
#     "http://127.0.0.1:3018",
#     "http://localhost",
# )

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",  # noqa: E501
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        # Errors logged by the SDK itself
        "sentry_sdk": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# Sentry
# ------------------------------------------------------------------------------
SENTRY_DSN = env.str("SENTRY_DSN", default="")
SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)

sentry_logging = LoggingIntegration(
    level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)
integrations = [
    sentry_logging,
    DjangoIntegration(),
    CeleryIntegration(),
    RedisIntegration(),
]
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=integrations,
        environment=env("SENTRY_ENVIRONMENT", default="development"),
        send_default_pii=True,
        traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.0),
    )
