import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY ='79qzfqu5fx(v)wur$-%rutqql@hj48uu^*j44@=zo_)ovtf0*q'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
DEBUG = True
