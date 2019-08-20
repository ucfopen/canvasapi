#!/bin/bash
set -e

PYTHON_VERSION=`python -c 'import sys; version=sys.version_info[:3]; print("{0}.{1}".format(*version))'`

major_ver=${PYTHON_VERSION:0:1}
minor_ver=${PYTHON_VERSION:2:3}

if (( "$major_ver" >= 3 && "$minor_ver" >= 6 )); then
	black --check canvasapi tests
fi
