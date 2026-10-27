import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

# Середовище запуску
DJANGO_ENV = os.getenv("DJANGO_ENV", "development").lower()

if DJANGO_ENV not in ("development", "production"):
    raise ImproperlyConfigured("DJANGO_ENV має бути development або production.")

# Секретний ключ зберігається поза кодом
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

if not SECRET_KEY or SECRET_KEY == "your-secret-key-here":
    raise ImproperlyConfigured(
        "Вкажіть DJANGO_SECRET_KEY у файлі .env або змінних оточення."
    )

# Налаштування dev / prod
DEBUG = os.getenv(
    "DJANGO_DEBUG",
    "true" if DJANGO_ENV == "development" else "false",
).lower() in ("true", "1", "yes")

if DJANGO_ENV == "production" and DEBUG:
    raise ImproperlyConfigured("У production DJANGO_DEBUG повинен бути False.")

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        "127.0.0.1,localhost" if DJANGO_ENV == "development" else "",
    ).split(",")
    if host.strip()
]

if DJANGO_ENV == "production" and not ALLOWED_HOSTS:
    raise ImproperlyConfigured(
        "У production необхідно налаштувати DJANGO_ALLOWED_HOSTS."
    )


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "django_filters",
    "learning",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
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
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
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


LANGUAGE_CODE = "uk"

TIME_ZONE = "Europe/Kyiv"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": ("rest_framework.pagination.PageNumberPagination"),
    "PAGE_SIZE": 5,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "EXCEPTION_HANDLER": ("learning.exceptions.custom_exception_handler"),
}


SPECTACULAR_SETTINGS = {
    "TITLE": "Online Learning Platform API",
    "DESCRIPTION": (
        "API платформи онлайн-навчання " "для роботи з курсами та уроками."
    ),
    "VERSION": "1.0.0",
    "COMPONENT_SPLIT_REQUEST": True,
}


MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

MAX_UPLOAD_SIZE = 5 * 1024 * 1024


# Кешування для зовнішніх REST-запитів
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "online-learning-cache",
        "TIMEOUT": 300,
    }
}


# Налаштування зовнішнього REST-сервісу
EXTERNAL_API_URL = os.getenv(
    "EXTERNAL_API_URL",
    "https://jsonplaceholder.typicode.com",
)

EXTERNAL_API_TIMEOUT = float(os.getenv("EXTERNAL_API_TIMEOUT", "5"))

EXTERNAL_API_CACHE_TIMEOUT = int(os.getenv("EXTERNAL_API_CACHE_TIMEOUT", "300"))


# Додаткові налаштування production
if DJANGO_ENV == "production":
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = os.getenv("DJANGO_SECURE_SSL_REDIRECT", "true").lower() in (
        "true",
        "1",
        "yes",
    )
