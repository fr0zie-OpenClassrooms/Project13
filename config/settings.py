import os
import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from dotenv import load_dotenv
from pathlib import Path
from django.contrib.messages import constants as messages

sentry_sdk.init(
    dsn="https://1548c90e148841c18fc10510e58b8970@o1116273.ingest.sentry.io/6525894",
    integrations=[
        DjangoIntegration(),
    ],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = "static/"
MEDIA_URL = "images/"
MEDIA_ROOT = os.path.join(BASE_DIR, "static/images")
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = True

ALLOWED_HOSTS = ["146.190.17.239", "coinspace.tech", "localhost"]

INSTALLED_APPS = [
    "home.apps.HomeConfig",
    "account.apps.AccountConfig",
    "tracker.apps.TrackerConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django_hosts",
]

MIDDLEWARE = [
    # "django_hosts.middleware.HostsRequestMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # "django_hosts.middleware.HostsResponseMiddleware",
]

ROOT_URLCONF = "config.urls"
# ROOT_HOSTCONF = "config.hosts"
# DEFAULT_HOST = "www"

MESSAGE_TAGS = {
    messages.ERROR: "alert alert-dismissible alert-danger",
    messages.SUCCESS: "alert alert-dismissible alert-success",
    messages.WARNING: "alert alert-dismissible alert-warning",
    messages.INFO: "alert alert-dismissible alert-info",
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            (os.path.join(BASE_DIR, "templates")),
        ],
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

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "coinspace",
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PWD"],
        "HOST": "localhost",
        "PORT": "5432",
    }
}

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES["default"].update(db_from_env)

AUTH_USER_MODEL = "account.User"
AUTHENTICATION_BACKENDS = ["account.backends.EmailBackend"]
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
LOGIN_URL = "/account/login"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
