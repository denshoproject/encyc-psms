# Django settings for psms project.

# add ./apps/ to path
import sys
from os import path
PROJECT_ROOT = path.dirname(path.abspath(__file__))
sys.path.append(path.join(PROJECT_ROOT, "apps"))

DEBUG = False
DEBUG = True
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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'psms:',
        'TIMEOUT': 60 * 15,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

STATIC_ROOT = '/var/www/psmsenv/encyc-psms/psms/static/'
MEDIA_ROOT  = '/var/www/html/psms/media/'
#STATIC_URL         = 'http://192.168.0.16/psms/static/'
#MEDIA_URL          = 'http://192.168.0.16/psms/media/'
STATIC_URL         = 'http://encyclopedia.densho.org/psms/static/'
MEDIA_URL          = 'http://encyclopedia.densho.org/psms/media/'
STATICFILES_DIRS = ('/var/www/psmsenv/encyc-psms/psms/static/',)

TEMPLATE_DIRS    = ('/var/www/psmsenv/encyc-psms/psms/templates/',)

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


# ----------------------------------------------------------------------

# jQuery
# ex: http://ajax.googleapis.com/ajax/libs/jquery/{{ JQUERY_VERSION }}/jquery.min.js
JQUERY_VERSION = '1.7'

# wikiprox
#WIKIPROX_MEDIAWIKI_API = 'http://beater/mediawiki/api.php'
#WIKIPROX_MEDIAWIKI_HTML = 'http://beater/mediawiki/index.php'
#WIKIPROX_MEDIAWIKI_HTML = 'http://10.0.4.15:9000/mediawiki/index.php'
#WIKIPROX_MEDIAWIKI_HTML = 'http://en.wikipedia.org/wiki'

# psms/tansu
PSMS_MEDIAWIKI_API = 'http://127.0.0.1:9000/mediawiki/api.php'
PSMS_MEDIAWIKI_USERNAME = 'gjost'
PSMS_MEDIAWIKI_PASSWORD = 'PASSWORD GOES HERE'
TANSU_API  = 'http://127.0.0.1:8080/api/v0.1'

# sources
EDITORS_MEDIAWIKI_URL = 'http://192.168.0.16:9066/mediawiki/index.php'
EDITORS_MEDIAWIKI_API = 'http://192.168.0.16:9000/mediawiki/api.php'
EDITORS_MEDIAWIKI_USER = ''
EDITORS_MEDIAWIKI_PASS = ''
SOURCES_HTTP_HOST = 'http://192.168.0.16:8080'

# ----------------------------------------------------------------------

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
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

TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = False
