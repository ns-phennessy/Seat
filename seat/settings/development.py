try:
    from shared import *
except:
    pass

SECRET_KEY = 'foobar'
ALLOWED_HOSTS = ['*']

DEBUG = True
TEMPLATE_DEBUG = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
