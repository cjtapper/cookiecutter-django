"""
Django settings for {{ cookiecutter.project_slug }} project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/stable/ref/settings/
"""

import datetime as dt
import os
import sys
from pathlib import Path

import dj_database_url
import dotenv
from django.core.exceptions import ImproperlyConfigured

MISSING = object()  # Sentinel value for missing kwargs


def env_var(var, default=MISSING):
    """
    Get the environment variable or return exception.
    """
    try:
        return os.environ[var]
    except KeyError:
        if default is not MISSING:
            return default
    raise ImproperlyConfigured(f"{var} environment variable must be set.")


def env_bool(var, default=MISSING):
    value = env_var(var, default)
    if isinstance(value, str):
        return value.lower() in {"true", "1"}
    return value


def env_int(var, default=MISSING):
    value = env_var(var, default)
    if isinstance(value, str):
        return int(value)
    return value


def env_list(var, default=MISSING):
    value = env_var(var, default)
    if isinstance(value, str):
        return value.split(",")
    return value


def env_tuple(var, default=MISSING):
    value = env_var(var, default)
    if isinstance(value, str):
        value = tuple(value.strip().strip("(").strip(")").split(","))
    return value


# 0. SETUP

BASE_DIR = Path(__file__).resolve().parent.parent

if "pytest" not in sys.modules:
    dotenv.load_dotenv(BASE_DIR / ".env")

# 1. DJANGO CORE SETTINGS
# https://docs.djangoproject.com/en/stable/ref/settings/#core-settings

SECRET_KEY = env_var(
    "DJANGO_SECRET_KEY",
    default="django-insecure--zs(!*1q))g1q#jaxtzqyzd6pqz!9b7-_!9o9c)-2g52pd%+h@",
)
DEBUG = env_bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", default=[])

CSRF_COOKIE_SECURE = env_bool("DJANGO_CSRF_COOKIE_SECURE", default=True)

DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:///db.sqlite3",
        conn_max_age=dt.timedelta(seconds=600).total_seconds(),
    ),
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEFAULT_FILE_STORAGE = env_var(
    "DJANGO_DEFAULT_FILE_STORAGE", default="django.core.files.storage.FileSystemStorage"
)

DEFAULT_FROM_EMAIL = env_var("DJANGO_DEFAULT_FROM_EMAIL", default="")

EMAIL_BACKEND = env_var(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)

INTERNAL_IPS = env_list("DJANGO_INTERNAL_IPS", default=[])

INSTALLED_APPS = [
    # First Party
    "{{ cookiecutter.project_slug }}.user_auth",
    # Third Party
    "debug_toolbar",
    # Contrib
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LANGUAGE_CODE = "en-us"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        "rich": {"datefmt": "[%X]"},
    },
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "filters": ["require_debug_true"],
            "formatter": "rich",
            "level": "DEBUG",
            "rich_tracebacks": True,
            "tracebacks_show_locals": True,
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

MEDIA_ROOT = env_var("DJANGO_MEDIA_ROOT", default="")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # According to the WhiteNoise documentation, the
    # WhiteNoiseMiddleware should be above all other middleware other
    # than the Django's SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "config.urls"

SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)

SECURE_HSTS_PRELOAD = env_bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)

SECURE_HSTS_SECONDS = env_int("DJANGO_SECURE_HSTS_SECONDS", default=0)

SECURE_PROXY_SSL_HEADER = env_tuple("DJANGO_SECURE_PROXY_SSL_HEADER", default=None)

SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", default=True)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["{{ cookiecutter.project_slug }}/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

WSGI_APPLICATION = "config.wsgi.application"


# 2.DJANGO CONTRIB SETTINGS

# django.contrib.auth
# https://docs.djangoproject.com/en/stable/ref/settings/#auth
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "user_auth.User"

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
]


# django.contrib.sessions
# https://docs.djangoproject.com/en/stable/ref/settings/#sessions
SESSION_COOKIE_SECURE = env_bool("DJANGO_SESSION_COOKIE_SECURE", default=True)

# django.contrib.staticfiles
# https://docs.djangoproject.com/en/3.2/ref/settings/#static-files
STATICFILES_DIRS = [
    BASE_DIR / "{{ cookiecutter.project_slug }}/static",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = "static"

STATIC_URL = "/static/"


# 3. THIRD PARTY SETTINGS


# 4. PROJECT SETTINGS
