SHELL := /bin/bash
BASEDIR = $(shell pwd)

.PHONY: build
build:
	rm -rf dist/* bing_images.egg-info build
	python3 -m build
testpypi:
	python3 -m twine upload -u __token__ --repository testpypi dist/*
pypi:
	python3 -m twine upload dist/*