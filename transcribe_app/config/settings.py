import os
from datetime import timedelta
from distutils.util import strtobool
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

path_to_env = os.path.join(BASE_DIR, "..", "infra", ".env")

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY", default=get_random_secret_key())

DEBUG = bool(strtobool(os.environ.get("DEBUG", default="True")))

ALLOWED_HOSTS = os.environ.get("HOST", default="127.0.0.1,localhost, testserver").split(
    ","
)

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "import_export",
    "rest_framework",
    "django_filters",
    "djoser",
    "rest_framework_simplejwt",
    "drf_yasg",
    "users.apps.UsersConfig",
    "transcription.apps.TranscriptionConfig",
    "api.apps.ApiConfig",
)

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = "config.urls"

TEMPLATES = (
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": (
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ),
        },
    },
)

WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": os.environ.get("POSTGRES_DB", default="postgres"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get("DB_HOST", default="db"),
        "PORT": os.environ.get("DB_PORT", default="5432"),
        "TIME_ZONE": TIME_ZONE,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": ("django.contrib.auth.password_validation." "MinimumLengthValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation." "CommonPasswordValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation." "NumericPasswordValidator"),
    },
]

AUTH_USER_MODEL = "users.User"

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "collected_static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=500),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=50),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {"basic": {"type": "basic"}},
}

YC_IAM_TOKEN = os.environ.get(
    "YC_IAM_TOKEN", default="AQVNzQZst92-SQYgP5zowxzTa7L6GrG0FT3OXhtZ"
)
YC_BUCKET_NAME = os.environ.get("YC_BUCKET_NAME", default="sefer")
TRANSCRIBE_API_URL = (
    "https://transcribe.api.cloud.yandex.net" "/speech/stt/v2/longRunningRecognize"
)

AWS_ACCESS_KEY_ID = os.environ.get(
    "AWS_ACCESS_KEY_ID", default="YCAJEM-ILuTzdEbu8c7Ozu3sf"
)
AWS_SECRET_ACCESS_KEY = os.environ.get(
    "AWS_SECRET_ACCESS_KEY", default="YCMrsyCpFN9iFBhb6GWkRnKp7_hpzk87Nx29jDif"
)
