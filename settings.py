# Django settings for autodata project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'mq%31q+sjj^)m^tvy(klwqw6ksv7du2yzdf9yn78iga*r%8w^t-httpxforwardedfor'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'httpxforwardedfor',
)

MIDDLEWARE_CLASSES = [
    'httpxforwardedfor.middleware.HttpXForwardedForMiddleware',
]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATIC_URL = '/static/'
