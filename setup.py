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
    license="BSD",
    zip_safe=False,
    keywords='django-httpxforwardedfor',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
