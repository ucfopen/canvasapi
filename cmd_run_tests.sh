#!/bin/bash
set -e

docker run --rm -v $(pwd):/app pycanvas coverage run -m unittest discover
docker run --rm -v $(pwd):/app pycanvas coverage xml
docker run --rm -v $(pwd):/app pycanvas pycodestyle pycanvas tests
docker run --rm -v $(pwd):/app pycanvas pyflakes pycanvas tests
