#!/bin/bash
set -e

docker run --rm -v $(pwd):/app canvasapi coverage run -m unittest discover
docker run --rm -v $(pwd):/app canvasapi coverage xml
docker run --rm -v $(pwd):/app canvasapi pycodestyle canvasapi tests
docker run --rm -v $(pwd):/app canvasapi pyflakes canvasapi tests
