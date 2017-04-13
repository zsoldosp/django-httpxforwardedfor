# Django settings for autodata project.

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

MIDDLEWARE_CLASSES = (
    'httpxforwardedfor.middleware.HttpXForwardedForMiddleware',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'mq%31q+sjj^)m^tvy(klwqw6ksv7du2yzdf9yn78iga*r%8w^t-httpxforwardedfor'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'httpxforwardedfor',
    'tests.testapp',
)

STATIC_URL = '/static/'

# Only allow HTTP_X_FORWARDED_FOR, if the request is marked as secure.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# To only allow change of the REMOTE_ADDR for requests via HTTPS.
# The default is to allow all requests.
TRUST_ONLY_HTTPS_PROXY = True
