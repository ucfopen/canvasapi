#!/bin/sh

coverage run -m unittest discover
coverage report
coverage html
flake8 canvasapi tests
mdl . .github
./scripts/run_black.sh
python scripts/alphabetic.py
