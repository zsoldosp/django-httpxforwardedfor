#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import httpxforwardedfor

from setuptools import setup

version = httpxforwardedfor.__version__

if sys.argv[-1] == 'publish':
    os.system('make release')
    sys.exit()

readme = open('README.rst').read()

description = "Set request.META['REMOTE_ADDR'] from request.META['HTTP_X_FORWARDED_FOR']"

setup(
    name='django-httpxforwardedfor',
    version=version,
    description=description,
    long_description=readme,
    author='Paessler AG',
    author_email='bis@paessler.com',
    url='https://github.com/PaesslerAG/django-httpxforwardedfor',
    packages=[
        'httpxforwardedfor',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.11,<=2.1',
        'IPy'
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-httpxforwardedfor',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
    ],
)
