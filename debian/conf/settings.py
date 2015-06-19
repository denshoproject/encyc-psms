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
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

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
TEMPLATE_DEBUG = DEBUG

SITE_ID = 2

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

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
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

SECRET_KEY = config.get('security', 'secret_key')


ADMINS = (
    ('Geoff Froh', 'geoff.froh@densho.org'),
    ('geoffrey jost', 'geoffrey.jost@densho.org'),
)
MANAGERS = ADMINS

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    #
    'django_extensions',
    'sorl.thumbnail',
    #
    'sources',
    'tansu',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates/'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'psms.urls'

# See http://docs.djangoproject.com/en/dev/topics/logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'DEBUG',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)-8s [%(module)s.%(funcName)s]  %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)-8s %(message)s'
        },
    },
    'filters': {
        # only log when settings.DEBUG == False
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/var/log/encyc/psms.log',
            'when': 'D',
            'backupCount': 14,
            'filters': [],
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'level': 'ERROR',
            'propagate': True,
            'handlers': ['mail_admins'],
        },
    },
    # This is the only way I found to write log entries from the whole DDR stack.
    'root': {
        'level': 'DEBUG',
        'handlers': ['file'],
    },
}

TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = False
