"""
Django settings for game_website project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.conf import global_settings
import dj_database_url
import os

# Directories to reference
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, 'game_website')

# Environment used for determinng configs
DJANGO_ENV = os.environ.setdefault('DJANGO_ENV', 'local').lower()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bk3xizz_pw95!=hl9m@3bmr(36xgrs927e3am@yuesa&4!d*k)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

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
if DJANGO_ENV == 'heroku':
    DATABASES = {'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))}
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "core", "static"),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(PROJECT_DIR, 'templates'),
    os.path.join(BASE_DIR, 'core', 'templates'),
    os.path.join(BASE_DIR, '..', 'core', 'templates'),
)

LOGIN_URL = 'core:login'
AUTH_USER_MODEL = 'core.User'
CRISPY_TEMPLATE_PACK = 'bootstrap3'

try:
    # Import any additional config files
    config = __import__('game_website.config.%s' % DJANGO_ENV, globals(), locals(), ['*'])
    lcl = locals()
    lcl.update({k: getattr(config, k) for k in dir(config) if not k.startswith('__')})
except ImportError:
    # No additional config file was found
    pass
