=============================
django-httpxforwardedfor
=============================

.. image:: https://badge.fury.io/py/django-httpxforwardedfor.png
    :target: https://badge.fury.io/py/django-httpxforwardedfor

.. image:: https://travis-ci.org/bis-team/django-httpxforwardedfor.png?branch=master
    :target: https://travis-ci.org/bis-team/django-httpxforwardedfor

.. image:: https://coveralls.io/repos/bis-team/django-httpxforwardedfor/badge.png?branch=master
    :target: https://coveralls.io/r/bis-team/django-httpxforwardedfor?branch=master

This middle-ware looks at the value of the header HTTTP_X_FORWARDED_FOR and
replaces the value of REMOTE_ADDR based on several conditions.

Quickstart
----------

Install django-httpxforwardedfor::

    pip install django-httpxforwardedfor

Then configure it in the settings of a project::

    # Make sure it is at the beginning of the list of middle-ware classes.
    # Only other middle-ware classes working on the remote address should
    # precede it.
    MIDDLEWARE_CLASSES = [
        'httpxforwardedfor.middleware.HttpXForwardedForMiddleware',
    ] + MIDDLEWARE_CLASSES

    # Only allow HTTP_X_FORWARDED_FOR, if the request is marked as secure.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # To only allow change of the REMOTE_ADDR for requests via HTTPS.
    # The default is to allow all requests.
    TRUST_ONLY_HTTPS_PROXY=True

Features
--------

* TODO
