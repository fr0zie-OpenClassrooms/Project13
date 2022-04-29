import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from django.contrib.messages import constants as messages

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.home.apps.HomeConfig",
    "apps.account.apps.AccountConfig",
    "apps.dashboard.data.apps.DataConfig",
    "apps.dashboard.tracker.apps.TrackerConfig",
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
        "ENGINE": "django.db.backends.mysql",
        "NAME": "coinspace",
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PWD"],
        "HOST": "localhost",
        "PORT": "3306",
    }
}

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

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
