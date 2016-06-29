#!/bin/bash
set -e

docker run --rm -v $(pwd):/app pycanvas python -m unittest discover
