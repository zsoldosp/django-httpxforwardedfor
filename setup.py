#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import httpxforwardedfor

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = httpxforwardedfor.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()

setup(
    name='django-httpxforwardedfor',
    version=version,
    description="""httpxforwardedfor description comes here""",
    long_description=readme,
    author='Paessler AG BIS Team',
    author_email='bis@paessler.com',
    url='https://gitlab.bis/bis-team/django-httpxforwardedfor',
    packages=[
        'httpxforwardedfor',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="",
    zip_safe=False,
    keywords='django-httpxforwardedfor',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
    ],
)
