from .base import *

DEBUG = False

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'cubedb.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cubedb',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': '3306',
    }
}
