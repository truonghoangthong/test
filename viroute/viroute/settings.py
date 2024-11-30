from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-9)pym!8*i7k=!ep6rx0d^$p@!fnzf*1($8ub10&(65h4(h!*7n'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'virouteapp.apps.VirouteappConfig',
    "rest_framework",
    "rest_framework.authtoken",
    'dj_rest_auth',
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    "oauth2_provider",
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'viroute.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'viroute.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default='mysql://root:NUrjwwbhLgunSnbpwQfEcMyGFtGFtaqy@autorack.proxy.rlwy.net:57334/railway'
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

OPENROUTE_API_KEY = '5b3ce3597851110001cf62481c184721ac24419cbc62a1f87c43d9dc'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

REST_USE_JWT = True
SITE_ID = 1

ACCOUNT_EMAIL_VERIFICATION = "none"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "APP": {
            "client_id": "Ov23li5qLxiU0WU7GNJc",
            "secret": "9643a077a202c2158e08dbb3fb4c42843c524032",
            "key": "",
            "redirect_uri": "http://127.0.0.1:8000/callback",
        }
    }
}

CORS_ALLOW_ALL_ORIGINS = False  # Không cho phép tất cả các origin, chỉ cho phép những origin được chỉ định
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Địa chỉ của frontend
    'https://test-production-2db4.up.railway.app',  # Địa chỉ của backend
]

CORS_ALLOW_CREDENTIALS = True  # Cho phép gửi cookies và thông tin xác thực

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'lelouchzero093@gmail.com'
EMAIL_HOST_PASSWORD = 'chithich1nguoi'
EMAIL_USE_TLS = True  # Chắc chắn bật TLS để mã hóa
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',  # Địa chỉ frontend
    'https://test-production-2db4.up.railway.app',  # Địa chỉ backend
]

CSRF_COOKIE_SAMESITE = 'None'  # Để hỗ trợ cross-site request (cần thiết cho frontend và backend khác domain)
CSRF_COOKIE_SECURE = True  # Đảm bảo cookie CSRF được gửi qua HTTPS (bật khi triển khai trên https)
