#!/bin/sh

coverage run -m unittest discover
coverage report
coverage html
flake8 canvasapi tests
mdl . .github
