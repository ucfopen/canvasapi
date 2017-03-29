#!/bin/bash
set -e

docker run --rm -v $(pwd):/app canvas-api coverage run -m unittest discover
docker run --rm -v $(pwd):/app canvas-api coverage xml
docker run --rm -v $(pwd):/app canvas-api pycodestyle canvas_api tests
docker run --rm -v $(pwd):/app canvas-api pyflakes canvas_api tests
