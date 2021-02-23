SHELL := /bin/bash
BASEDIR = $(shell pwd)

.PHONY: build
build:
	rm -rf dist/*
	python3 -m build
testpypi:
	python3 -m twine upload --repository testpypi dist/*
pypi:
	python3 -m twine upload dist/*