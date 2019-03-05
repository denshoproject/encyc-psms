"""
Django settings for encyc-psms project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import ConfigParser
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, '..', 'VERSION'), 'r') as f:
    VERSION = f.read()

# User-configurable settings are located in the following files.
# Files appearing *later* in the list override earlier files.
CONFIG_FILES = [
    '/etc/encyc/psms.cfg',
    '/etc/encyc/psms-local.cfg'
]
config = ConfigParser.ConfigParser()
configs_read = config.read(CONFIG_FILES)
if not configs_read:
    raise Exception('No config file!')

# ----------------------------------------------------------------------

DEBUG = config.get('debug', 'debug')

SITE_ID = 2

WSGI_APPLICATION = 'psms.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': config.get('database', 'engine'),
        'HOST': config.get('database', 'host'),
        'PORT': config.get('database', 'port'),
        'NAME': config.get('database', 'name'),
        'USER': config.get('database', 'user'),
        'PASSWORD': config.get('database', 'password'),
    }
}
#update django_site set domain='10.0.4.15:8000', name='densho front' where id=1;
#insert into django_site (domain, name) values ('10.0.4.15:8080', 'densho psms');

STATIC_ROOT = config.get('media', 'static_root')
STATIC_URL = config.get('media', 'static_url')
MEDIA_ROOT = config.get('media', 'media_root')
MEDIA_URL = config.get('media', 'media_url')

# jQuery
# ex: http://ajax.googleapis.com/ajax/libs/jquery/{{ JQUERY_VERSION }}/jquery.min.js
JQUERY_VERSION = '1.7'

# psms/tansu
PSMS_MEDIAWIKI_API = config.get('psms', 'mediawiki_api')
PSMS_MEDIAWIKI_USERNAME = config.get('psms', 'mediawiki_username')
PSMS_MEDIAWIKI_PASSWORD = config.get('psms', 'mediawiki_password')
TANSU_API  = config.get('psms', 'tansu_api')

# sources
EDITORS_MEDIAWIKI_URL = config.get('sources', 'mediawiki_url')
EDITORS_MEDIAWIKI_API = config.get('sources', 'mediawiki_api')
EDITORS_MEDIAWIKI_USER = config.get('sources', 'mediawiki_username')
EDITORS_MEDIAWIKI_PASS = config.get('sources', 'mediawiki_password')
SOURCES_HTTP_HOST = config.get('sources', 'http_host')

CACHES = {
    'default': {
#        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'psms:',
        'TIMEOUT': 60 * 15,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

# ----------------------------------------------------------------------

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    host.strip()
    for host in config.get('security', 'allowed_hosts').strip().split(',')
]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('security', 'secret_key')


ADMINS = (
    ('Geoff Froh', 'geoff.froh@densho.org'),
    ('geoffrey jost', 'geoffrey.jost@densho.org'),
)
MANAGERS = ADMINS

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #
    'django_extensions',
    'drf_yasg',
    'rest_framework',
    'sorl.thumbnail',
    #
    'sources',
    'tansu',
]

API_BASE = '/api/2.0/'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'PAGE_SIZE': 20,
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(
                os.path.dirname(BASE_DIR),
                'venv/psms/lib/python2.7/site-packages',
                'django/contrib/admin/templates',
            )
        ],
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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'psms.urls'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/1.11/topics/i18n/
TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = False
USE_TZ = True
