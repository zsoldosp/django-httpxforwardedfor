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
    MIDDLEWARE_CLASSES = [
        'httpxforwardedfor.middleware.HttpXForwardedForMiddleware',
    ] + MIDDLEWARE_CLASSES

    # Only allow HTTP_X_FORWARDED_FOR, if the request is marked as secure.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # To only allow change of the REMOTE_ADDR for requests via HTTPS.
    # The default is to allow all requests.
    TRUST_ONLY_HTTPS_PROXY=True

Release Notes
-------------

* 0.1.2 - initial public release

  * supports Django 1.8 to 1.11 on Python 2.7, 3.3, 3.4, and 3.5
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
    for version in 3.3 3.5; do
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
