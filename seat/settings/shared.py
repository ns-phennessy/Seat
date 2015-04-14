
import sys
import os

# 2 levels up from this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

ROOT_URLCONF = 'seat.urls'
WSGI_APPLICATION = 'seat.wsgi.application'

#LDAP
LDAP_HOST = 'ldap://ldap.patcave.info'
LDAP_ROOT_SEARCH_DN = 'dc=ldap,dc=patcave,dc=info'# we happen to log in as the root node when testing
LDAP_DISPLAY_NAME_ATTR = 'givenName'
LDAP_MAIL_ATTR = 'mail'

# Applications
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'seat',
    'dashboard',
    'login',
    'student',
    'api',
)

# Middleware
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'seat.middleware.methods.HttpPostTunnelingMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'seat.middleware.methods.HttpPostTunnelingMiddleware',
	#'seat.middleware.exceptions.ExceptionMiddleware'
)

# Template Settings
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# Static Files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'INFO',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "debug.log"),
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'dashboard': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
        },
        'login': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
        },
        'api':{
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
        }
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = True
