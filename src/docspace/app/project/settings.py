from pathlib import Path
import django
from docspace import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config['DJANGO_SECRET_KEY']

DEBUG = bool(config['DEBUG'])

ALLOWED_HOSTS = config['DJANGO_ALLOWED_HOSTS'].split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'docspace.app.core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'docspace.app.project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'docspace.app.project.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'docspace',
        'USER': config['POSTGRES_USERNAME'],
        'PASSWORD': config['POSTGRES_PASSWORD'],
        'HOST': config['POSTGRES_HOST'],
        'PORT': config['POSTGRES_PORT'],
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

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
LOGIN_URL = 'core:login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_DIRS = [BASE_DIR / 'static']

STATIC_URL = 'static/'

STATICFILES_STORAGE = 'docspace.app.core.storage.StaticStorage'

DEFAULT_FILE_STORAGE = 'docspace.app.core.storage.MediaStorage'

AWS_S3_REGION_NAME = 'nyc3'

AWS_S3_ENDPOINT_URL = f'https://docspace.{AWS_S3_REGION_NAME}.digitaloceanspaces.com'

AWS_ACCESS_KEY_ID = config['S3_ACCESS_KEY']

AWS_SECRET_ACCESS_KEY = config['S3_SECRET_KEY']

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
