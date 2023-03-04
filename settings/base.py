import os
from datetime import timedelta
from pathlib import Path
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env.read_env(os.path.join(BASE_DIR, '.env'), overwrite=True)
SECRET_KEY = env('SECRET_KEY')
ENVIRONMENT = env('ENVIRONMENT')
ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

CUSTOM_APPS = [
    'authentication',
    'job_portal',
    'dashboard'
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'django_filters'
]


INSTALLED_APPS += CUSTOM_APPS + THIRD_PARTY_APPS

# Defining Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

THIRD_PARTY_MIDDLEWARES = [
]

CUSTOM_MIDDLEWARES = [
]

MIDDLEWARE += CUSTOM_MIDDLEWARES + THIRD_PARTY_MIDDLEWARES

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'settings.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },

]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    # os.path.join(BASE_DIR, 'staticfiles'),
]

# Add these new lines

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "authentication.User"

# Django Cors Settings
CORS_ALLOW_ALL_ORIGINS = True

# DRF Configurations
SIMPLE_JWT = {
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=800),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
}

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        # 'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    # API Throttling
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '10/minute',
    #     'user': '10/minute'
    # },
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    # 'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ]
}

# Email Configurations
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': None
}

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = True
FROM_EMAIL = env('FROM_EMAIL')

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

REACT_APP_URL = env('REACT_APP_URL')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
CHATGPT_API_KEY = env('CHATGPT_API_KEY')