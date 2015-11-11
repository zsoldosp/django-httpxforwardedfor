.PHONY: clean-pyc clean-build docs clean-tox
PYPI_SERVER?=http://pypi.ipx.bis/simple/
SHELL=/bin/bash

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "testall - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean: clean-build clean-pyc clean-tox

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 httpxforwardedfor tests

test:
	python manage.py test httpxforwardedfor

clean-tox:
	if [[ -d .tox ]]; then rm -r .tox; fi

test-all: clean-tox
	tox

coverage:
	coverage run --source httpxforwardedfor setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/django-httpxforwardedfor.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ django-httpxforwardedfor
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release: VERSION=$(shell python -c"import httpxforwardedfor as m; print m.__version__")
release: TAG:=v${VERSION}
release: TAG_URL:=$(shell git remote -v | grep origin | sed "s/[\t ]\+/ /g" | cut -d' ' -f 2 | sort -u| sed "s/git@//" | sed "s/:/\//" | sed "s/\.git$$/\/tree\/${TAG}/")
release: TAG_HTTP_STATUS:=$(shell wget ${TAG_URL} -O - --no-check-certificate 2>&1 | grep "200 OK" | wc -l)
	if [[ 0 -eq ${TAG_HTTP_STATUS} ]]; then git tag -am "tag v${VERSION}" ${TAG}; git push --tags origin; fi
release: clean
	echo "if the release fails, setup a ~/pypirc file as per https://docs.python.org/2/distutils/packageindex.html#pypirc"
	python setup.py sdist upload -r ${PYPI_SERVER}
	python setup.py bdist_wheel upload -r ${PYPI_SERVER}

sdist: clean
	python setup.py sdist
	ls -l dist
