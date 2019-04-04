=============================
django-httpxforwardedfor
=============================

.. image:: https://travis-ci.org/PaesslerAG/django-httpxforwardedfor.svg?branch=master
        :target: https://travis-ci.org/PaesslerAG/django-httpxforwardedfor

----

.. contents:: Set request.META['REMOTE_ADDR'] from request.META['HTTP_X_FORWARDED_FOR']

----

Quickstart
----------

Install django-httpxforwardedfor::

    pip install django-httpxforwardedfor

Configure it in the settings of your django project::

    # Make sure it is at the beginning of the list of middle-ware classes.
    # Only other middle-ware classes working on the remote address should
    # precede it.
    MIDDLEWARE = [
        'httpxforwardedfor.middleware.HttpXForwardedForMiddleware',
    ] + MIDDLEWARE

    # Only allow HTTP_X_FORWARDED_FOR, if the request is marked as secure.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # To only allow change of the REMOTE_ADDR for requests via HTTPS.
    # The default is to allow all requests.
    TRUST_ONLY_HTTPS_PROXY = True


Release Notes
-------------

* 0.3.1 - dropping support for Python 3.4 as it ran into EOL in March19

* 0.3.0 - update supported versions according to
  https://www.djangoproject.com/download/#supported-versions and
  https://devguide.python.org/#status-of-python-branches

  * dropping support for Django 1.10 and Python 3.2 and 3.3
  * adding support for Python 3.7
  * adding support for Django 2.0
  * adding support for Django 2.1

* 0.2.0 - futureproof release

  * adapt to new middleware format of django 1.10+
  * drop support for python 3.3, django < 1.10

* 0.1.2 - initial release

  * supports Django 1.8, 1.9, 1.10, 1.11 on python 2.7, 3.3, 3.4, 3.5, and 3.6 - as per the
    `official django docs <https://docs.djangoproject.com/en/dev/faq/install/#what-python-version-can-i-use-with-django>`_
  * configuration to activate forwarding of header only for safe requests and trusting only https requests in general.


.. contributing start

Contributing
------------

As an open source project, we welcome contributions.

The code lives on `github <https://github.com/PaesslerAG/django-httpxforwardedfor>`_.

Reporting issues/improvements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please open an `issue on github <https://github.com/PaesslerAG/django-httpxforwardedfor/issues/>`_
or provide a `pull request <https://github.com/PaesslerAG/django-httpxforwardedfor/pulls/>`_
whether for code or for the documentation.

For non-trivial changes, we kindly ask you to open an issue, as it might be rejected.
However, if the diff of a pull request better illustrates the point, feel free to make
it a pull request anyway.

Pull Requests
~~~~~~~~~~~~~

* for code changes

  * it must have tests covering the change. You might be asked to cover missing scenarios
  * the latest ``flake8`` will be run and shouldn't produce any warning
  * if the change is significant enough, documentation has to be provided

Setting up all Python versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    sudo apt-get -y install software-properties-common
    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    for version in 3.5 3.6 3.7; do
      py=python$version
      sudo apt-get -y install ${py} ${py}-dev
    done

Code of Conduct
~~~~~~~~~~~~~~~

As it is a Django extension, it follows
`Django's own Code of Conduct <https://www.djangoproject.com/conduct/>`_.
As there is no mailing list yet, please just email one of the main authors
(see ``setup.py`` file or `github contributors`_)


.. contributing end


.. _github contributors: https://github.com/PaesslerAG/django-httpxforwardedfor/graphs/contributors
