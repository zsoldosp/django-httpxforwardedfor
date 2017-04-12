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
    author='Paessler AG BIS Team',
    author_email='bis@paessler.com',
    url='https://github.com/PaesslerAG/django-httpxforwardedfor',
    packages=[
        'httpxforwardedfor',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.8,<=1.11',
        'IPy',
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
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
    ],
)
