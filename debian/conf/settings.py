# Django settings for psms project.

# add ./apps/ to path
import sys
from os import path
PROJECT_ROOT = path.dirname(path.abspath(__file__))
sys.path.append(path.join(PROJECT_ROOT, "apps"))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SITE_ID = 2
SECRET_KEY = 'SECRET KEY HERE'

ADMINS = (
    ('Geoff Froh', 'geoff.froh@densho.org'),
    ('geoffrey jost', 'geoffrey.jost@densho.org'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'PORT': 3306,
        'NAME': 'psms',
        'USER': 'psms',
        'PASSWORD': 'PASSWORD GOES HERE',
    }
}
#update django_site set domain='10.0.4.15:8000', name='densho front' where id=1;
#insert into django_site (domain, name) values ('10.0.4.15:8080', 'densho psms');

STATIC_ROOT = '/var/www/psmsenv/encyc-psms/psms/static/'
MEDIA_ROOT = '/var/www/html/psms/media/'
STATIC_URL = 'http://encyclopedia.densho.org/psms/static/'
MEDIA_URL = 'http://encyclopedia.densho.org/psms/media/'

# jQuery
# ex: http://ajax.googleapis.com/ajax/libs/jquery/{{ JQUERY_VERSION }}/jquery.min.js
JQUERY_VERSION = '1.7'

# psms/tansu
PSMS_MEDIAWIKI_API = 'http://127.0.0.1:9000/mediawiki/api.php'
PSMS_MEDIAWIKI_USERNAME = 'psmsbot'
PSMS_MEDIAWIKI_PASSWORD = 'PASSWORD GOES HERE'
TANSU_API  = 'http://127.0.0.1:8080/api/v0.1'

# sources
EDITORS_MEDIAWIKI_URL = 'http://192.168.0.16:9066/mediawiki/index.php'
EDITORS_MEDIAWIKI_API = 'http://192.168.0.16:9000/mediawiki/api.php'
EDITORS_MEDIAWIKI_USER = 'psmsbot'
EDITORS_MEDIAWIKI_PASS = 'PASSWORD GOES HERE'
SOURCES_HTTP_HOST = 'http://192.168.0.16:8080'

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
    'core',
    'sources',
    'tansu',
)

STATICFILES_DIRS = (
    '/var/www/psmsenv/encyc-psms/psms/static/',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_DIRS = (
    '/var/www/psmsenv/encyc-psms/psms/templates/',
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
