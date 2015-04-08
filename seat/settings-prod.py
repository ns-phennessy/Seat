try:
    from settings import *
except:
    pass

# Database
DATABASES = {
    'default':{
        'NAME'      : 'seat',
        'ENGINE'    : 'django.db.backends.mysql',
        'USER'      : 'capstone',
        'PASSWORD'  : '9324d1eb',
        'HOST'      : '',
        'PORT'      : ''
    }
}
