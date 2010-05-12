import os

ENVIRONMENT = "unknown"
try:
    if os.environ["SERVER_SOFTWARE"].lower().startswith("dev"):
        ENVIRONMENT = "local"
    elif os.environ["SERVER_SOFTWARE"].lower().startswith("google apphosting"):
        ENVIRONMENT = "hosted"
except:
    pass

DEBUG = (ENVIRONMENT == "local")
DEBUG = True

ADMINS = (
    ('Mike Koss', 'mckoss@startpad.org'),
    ('Roy Leban', 'roy@royleban.com'),
)

"""
reqfilter customization strings
"""
sSiteName = "ThApp"
sSiteDomain = "thapp.appspot.com"
sSiteHost = sSiteDomain
sJSNamespace = "THAPP"
sTwitterSource = "Kahnsept"
sTwitterUser = "kahnsept"
sSiteTitle = "A sample application for Kahnsept"
sSiteTagline = "It's a useful application for managing the Theta Chi fraternity."
sSecretName = "secret.1"
sAnalyticsCode = "UA-8981361-1"
sAdPublisherID = "ca-pub-0345330507104463"  # AdSense/AdManager

MANAGERS = ADMINS

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


TIME_ZONE = 'PST8PDT US'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'reqfilter.ReqFilter',
    'mixins.CacheFilter'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'reqfilter.GetContext',
    'jscomposer.GetContext',
    )

# For django.middleware.common.CommonMiddleware
APPEND_SLASH = False
PREPEND_WWW = False

ROOT_URLCONF = 'urls'

import os.path
dirHome = os.path.dirname(__file__)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(dirHome, 'templates').replace('\\', '/'),
)

CACHE_MIDDLEWARE_SECONDS = 7*24*60*60

INSTALLED_APPS = (
    # TODO Are these two really used?
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.humanize',
    'jscomposer',
    'reqfilter',
)

# For jscomposer
SCRIPT_DIR = os.path.join(dirHome, 'scripts').replace('\\', '/')
SCRIPT_DEBUG = DEBUG
#SCRIPT_DEBUG = False
SCRIPT_COMBINE = not SCRIPT_DEBUG
SCRIPT_VERSION = os.environ['CURRENT_VERSION_ID']
SCRIPT_CACHE = not SCRIPT_DEBUG
SCRIPT_ALIASES = {
    'thapp':['namespace', 'base', 'json2', 'timer', 'vector', 'dom',
                 'cookies', 'events', 'data', 'dateutil', 'main'],
    }

#TEMPLATE_STRING_IF_INVALID = "***ERROR***"
