[![CanvasAPI on PyPI](https://img.shields.io/pypi/v/canvasapi.svg)](https://pypi.python.org/pypi/canvasapi)
[![License](https://img.shields.io/pypi/l/canvasapi.svg)](https://pypi.python.org/pypi/canvasapi)
[![Python Versions](https://img.shields.io/pypi/pyversions/canvasapi.svg)](https://pypi.python.org/pypi/canvasapi)
[![Documentation Status](https://readthedocs.org/projects/canvasapi/badge/?version=stable)](http://canvasapi.readthedocs.io/en/stable/?badge=stable)
[![Build Status](https://github.com/ucfopen/canvasapi/actions/workflows/run-tests.yml/badge.svg?branch=develop)](https://github.com/ucfopen/canvasapi/actions)
[![codecov](https://codecov.io/gh/ucfopen/canvasapi/branch/develop/graph/badge.svg?token=CFNpp8f56M)](https://codecov.io/gh/ucfopen/canvasapi)
[![Join UCF Open Slack Discussions](https://badgen.net/badge/icon/ucfopen?icon=slack&label=slack&color=pink)](https://dl.ucf.edu/join-ucfopen)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# CanvasAPI

CanvasAPI is a Python library for accessing Instructure’s [Canvas LMS API](https://canvas.instructure.com/doc/api/index.html). The library enables developers to programmatically manage Canvas courses, users, gradebooks, and more.

## Table of Contents

* [CanvasAPI](#canvasapi)
    * [Table of Contents](#table-of-contents)
    * [Installation](#installation)
    * [Documentation](#documentation)
    * [Contributing](#contributing)
    * [Quickstart](#quickstart)
        * [Working with Canvas Objects](#working-with-canvas-objects)
            * [Course objects](#course-objects)
            * [User objects](#user-objects)
            * [Paginated Lists](#paginated-lists)
            * [Keyword arguments](#keyword-arguments)
    * [CanvasAPI Projects](#canvasapi-projects)
    * [Contact Us](#contact-us)

## Installation

You can install CanvasAPI with pip:

`pip install canvasapi`

## Documentation

Full documentation is available at [Read the Docs](http://canvasapi.readthedocs.io/).

## Contributing

Want to help us improve CanvasAPI? Check out our [Contributing Guide](.github/CONTRIBUTING.md) to learn about running CanvasAPI as a developer, picking issues to work on, submitting bug reports, contributing patches, and more.

## Quickstart

Getting started with CanvasAPI is easy.

Like most API clients, CanvasAPI exposes a single class that provides access to the rest of the API: `Canvas`.

The first thing to do is instantiate a new `Canvas` object by providing your Canvas instance’s root API URL and a valid API key:

```python
# Import the Canvas class
from canvasapi import Canvas

# Canvas API URL
API_URL = "https://example.com"
# Canvas API key
API_KEY = "p@$$w0rd"

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)
```

You can now use `canvas` to begin making API calls.

### Working with Canvas Objects

CanvasAPI converts the JSON responses from the Canvas API into Python objects. These objects provide further access to the Canvas API. You can find a full breakdown of the methods these classes provide in our [class documentation](http://canvasapi.readthedocs.io/en/stable/class-reference.html). Below, you’ll find a few examples of common CanvasAPI use cases.

#### Course objects

Courses can be retrieved from the API:

```python
# Grab course 123456
>>> course = canvas.get_course(123456)

# Access the course's name
>>> course.name
'Test Course'

# Update the course's name
>>> course.update(course={'name': 'New Course Name'})
```

See our documentation on [keyword arguments](#keyword-arguments) for more information about how `course.update()` handles the `name` argument.

#### User objects

Individual users can be pulled from the API as well:

```python
# Grab user 123
>>> user = canvas.get_user(123)

# Access the user's name
>>> user.name
'Test User'

# Retrieve a list of courses the user is enrolled in
>>> courses = user.get_courses()

# Grab a different user by their SIS ID
>>> login_id_user = canvas.get_user('some_user', 'sis_login_id')
```

#### Paginated Lists

Some calls, like the `user.get_courses()` call above, will request multiple objects from Canvas’s API. CanvasAPI collects these objects in a `PaginatedList` object. `PaginatedList` generally acts like a regular Python list. You can grab an element by index, iterate over it, and take a slice of it.

**Warning**: `PaginatedList` lazily loads its elements. Unfortunately, there’s no way to determine the exact number of records Canvas will return without traversing the list fully. This means that `PaginatedList` isn’t aware of its own length and negative indexing is not currently supported.

Let’s look at how we can use the `PaginatedList` returned by our `get_courses()` call:

```python
# Retrieve a list of courses the user is enrolled in
>>> courses = user.get_courses()

>>> print(courses)
<PaginatedList of type Course>

# Access the first element in our list.
#
# You'll notice the first call takes a moment, but the next N-1
# elements (where N = the per_page argument supplied; the default is 10)
# will be instantly accessible.
>>> print(courses[0])
TST101 Test Course (1234567)

# Iterate over our course list
>>> for course in courses:
         print(course)

TST101 Test Course 1 (1234567)
TST102 Test Course 2 (1234568)
TST103 Test Course 3 (1234569)

# Take a slice of our course list
>>> courses[:2]
[TST101 Test Course 1 (1234567), TST102 Test Course 2 (1234568)]
```

#### Keyword arguments

Most of Canvas’s API endpoints accept a variety of arguments. CanvasAPI allows developers to insert keyword arguments when making calls to endpoints that accept arguments.

```python
# Get all of the active courses a user is currently enrolled in
>>> courses = user.get_courses(enrollment_state='active')
```

For a more detailed description of how CanvasAPI handles more complex keyword arguments, check out the [Keyword Argument Documentation](http://canvasapi.readthedocs.io/en/stable/keyword-args.html).

## CanvasAPI Projects

Since its initial release in June 2016, CanvasAPI has amassed over 100 [dependent repositories](https://github.com/ucfopen/canvasapi/network/dependents). Many of these include various tools used to enhance the Canvas experience for both instructors and students. Here are a few popular repositories that use CanvasAPI:

* [Canvas Grab](https://github.com/skyzh/canvas_grab)
    * Canvas Grab is the most popular project using CanvasAPI. This tool, with one click, copies all files from Canvas LMS to local directory. CanvasAPI is used in this project to connect to a course and grab its files.
* [Clanvas](https://github.com/marklalor/clanvas)
    * Clanvas is a command-line client for Canvas. It uses the already available bash commands plus some additional ones to interact with various features of Canvas from the commmand line.
* [CS221Bot](https://github.com/Person314159/cs221bot)
    * CS221Bot is a Discord bot for the CPCS 221 course at University of British Columbia. CanvasAPI is used in this project to connect to and synchronize with a course and get its data, such as announcements, new assignments, and more.

If you have a project that uses CanvasAPI that you'd like to promote, please contact us!

## Contact Us

Need help? Have an idea? Feel free to check out our [Discussions](https://github.com/ucfopen/canvasapi/discussions) board. Just want to say hi or get extended spport? Come join us on the [UCF Open Slack Channel](https://dl.ucf.edu/join-ucfopen) and join the `#canvasapi` channel!
