import re
from os import path

from setuptools import setup

# get version number
with open("canvasapi/__init__.py", "r") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("Cannot find version information")

# Get the PyPI package info from the readme
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="canvasapi",
    version=version,
    description="API wrapper for the Canvas LMS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ucfopen/canvasapi",
    author="University of Central Florida - Center for Distributed Learning",
    author_email="techrangers@ucf.edu",
    license="MIT License",
    packages=["canvasapi"],
    include_package_data=True,
    install_requires=["arrow", "pytz", "requests"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
    ],
)
