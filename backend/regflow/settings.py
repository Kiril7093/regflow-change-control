from pathlib import Path
import os

from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR.parent / ".env")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "xI63eUxETOwFCNs_zwdG8A0i3trdUBJ0DYjJsp6djXDmEEC0YkcnGw")
DEBUG = os.getenv("DEBUG", "0") == "1"

ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]

INSTALLED_APPS = [
    "core",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "regflow.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "regflow.wsgi.application"

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=60),
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
