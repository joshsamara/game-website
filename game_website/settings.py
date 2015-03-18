"""
Django settings for game_website project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.conf import global_settings
import os
from game_website import local_settings
from django.core.urlresolvers import reverse

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, 'game_website')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bk3xizz_pw95!=hl9m@3bmr(36xgrs927e3am@yuesa&4!d*k)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

DJANGO_ENV = os.environ.setdefault('DJANGO_ENV', 'local').lower()

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'core',
    'stdimage',
    'crispy_forms'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'game_website.urls'

WSGI_APPLICATION = 'game_website.wsgi.application'

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

ADDITIONAL_TEMPLATE_CONTEXT_PROCESSORS = (
    'game_website.context_processors.default_context_processor',
)
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + ADDITIONAL_TEMPLATE_CONTEXT_PROCESSORS

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
# TODO: Set up individiual settings files
if DJANGO_ENV == 'travis':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'travisdb',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'gamesite',
            'USER': 'gameadmin',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'core.User'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "core", "static"),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(PROJECT_DIR, 'templates'),
    os.path.join(BASE_DIR, 'core', 'templates'),
)

LOGIN_URL = 'core:login'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

AWS_STORAGE_BUCKET_NAME = 'gamewebsitebucket'
AWS_ACCESS_KEY_ID = local_settings.AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = local_settings.AWS_SECRET_KEY
AWS_S3_HOST = 's3-us-west-2.amazonaws.com'
# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'game_website.custom_storages.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'rushmanager.custom_storages.MediaStorage'
