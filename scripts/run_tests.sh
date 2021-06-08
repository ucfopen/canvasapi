#!/bin/sh

coverage run -m unittest discover
coverage report
coverage html
black --check canvasapi tests
isort --check canvasapi tests
flake8 canvasapi tests
mdl . .github
python scripts/alphabetic.py
python scripts/find_missing_kwargs.py
