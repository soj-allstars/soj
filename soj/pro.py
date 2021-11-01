from .settings import *

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY', '-h0m96a@zxm57o_wej@b^dq-+jsmx9o1v2z++k)yq8^i*1+f9g')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'soj',
        'USER': 'soj',
        'PASSWORD': os.environ.get('DB_PASSWORD', 'soj'),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [
                {
                    'address': (os.environ.get('REDIS_HOST', '127.0.0.1'), os.environ.get('REDIS_PORT', 6379)),
                    'db': 1,
                    'password': os.environ.get('REDIS_PASSWORD', None)
                }
            ]
        },
    },
}

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = False

STATIC_ROOT = os.path.join(BASE_DIR, 'shared_data/static_files')

LOGGING = {}
