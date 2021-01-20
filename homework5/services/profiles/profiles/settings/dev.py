from .base import *


ALLOWED_HOSTS = ['profiles_service', 'localhost', '0.0.0.0', '*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': 'postgres',
        'PORT': '5432',
    }
}
