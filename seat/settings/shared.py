
import sys
import os

# 2 levels up from this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

ROOT_URLCONF = 'seat.urls'
WSGI_APPLICATION = 'seat.wsgi.application'

#LDAP---------->
LDAP_HOST = 'ldap://ldap.patcave.info'   # Server to connect to
LDAP_STAFF_ORGANIZATIONAL_UNIT = 'staff' # OU for teachers
LDAP_STUDENT_ORGANIZATIONAL_UNIT = 'students' # OU for students

# LDAP is a b-tree type thing (its really a big directory structure) this is the root directory
LDAP_STAFF_SEARCH_DN = 'ou='+LDAP_STAFF_ORGANIZATIONAL_UNIT+',ou=users,dc=ldap,dc=patcave,dc=info'  
LDAP_STUDENT_SEARCH_DN = 'ou='+LDAP_STUDENT_ORGANIZATIONAL_UNIT+',ou=users,dc=ldap,dc=patcave,dc=info'  

#TODO: when we deploy to using LDAP, cn 
# should become sAMAccountName per
# http://stackoverflow.com/questions/29641901/ldap-and-ad-are-we-always-allowed-to-search/29642063#29642063
LDAP_FILTER = 'cn=%s' # LDAP search filter: we replace %s with the username given in login

LDAP_DISPLAY_NAME_ATTR = 'givenName'    # Attribute to be used as the user's display name
LDAP_MAIL_ATTR = 'mail'                 # Attribute to be used to get the user's email

# we have to authenticate with AD to even search the tree.
# in the school system this will probably be a new user
# just for this application
# -> change this when deploying to school
LDAP_APP_USER = 'cn=admin,dc=ldap,dc=patcave,dc=info' # this is the DN for a user who can search and read the tree, but not modify it
LDAP_APP_PASS = 'takeaseat!'                          # this is the password for the user who is searching the tree
#LDAP------------< 

SESSION_COOKIE_SECURE = False

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
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
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
        'applications': {
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
