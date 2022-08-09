Getting Started with CanvasAPI
===============================

Installing CanvasAPI
---------------------

You can install CanvasAPI with pip::

    pip install canvasapi

Usage
-----

Before using CanvasAPI, you'll need to instantiate a new Canvas object:

.. code:: python

    # Import the Canvas class
    from canvasapi import Canvas

    # Canvas API URL
    API_URL = "https://example.com"
    # Canvas API key
    API_KEY = "p@$$w0rd"

    # Initialize a new Canvas object
    canvas = Canvas(API_URL, API_KEY)

You can now use :code:`canvas` to make API calls.

Working with Canvas Objects
---------------------------

CanvasAPI converts the JSON responses from the Canvas API into Python objects. These objects provide further access to the Canvas API. You can find a full breakdown of the methods these classes provide in our `class documentation <class-reference.html>`_. Below, you’ll find a few examples of common CanvasAPI use cases.

Course objects
~~~~~~~~~~~~~~

Courses can be retrieved from the API:

.. code:: python

    # Grab course 123456
    >>> course = canvas.get_course(123456)

    # Access the course's name
    >>> course.name
    'Test Course'

    # Update the course's name
    >>> course.update(course={'name': 'New Course Name'})

See our documentation on `keyword arguments`_ for more information about how :code:`course.update()` handles the :code:`name` argument.

User objects
~~~~~~~~~~~~

.. code:: python

    # Grab user 123
    >>> user = canvas.get_user(123)

    # Access the user's name
    >>> user.name
    'Test User'

    # Retrieve a list of courses the user is enrolled in
    >>> courses = user.get_courses()

    # Grab a different user by their SIS ID
    >>> login_id_user = canvas.get_user('some_user', 'sis_login_id')

Paginated Lists
~~~~~~~~~~~~~~~

Some calls, like the :code:`user.get_courses()` call above, will request multiple objects from Canvas’s API. CanvasAPI collects these objects in a :code:`PaginatedList` object. :code:`PaginatedList` generally acts like a regular Python list. You can grab an element by index, iterate over it, and take a slice of it.

**Warning**: :code:`PaginatedList` lazily loads its elements. Unfortunately, there’s no way to determine the exact number of records Canvas will return without traversing the list fully. This means that :code:`PaginatedList` isn’t aware of its own length and negative indexing is not currently supported.

Let’s look at how we can use the :code:`PaginatedList` returned by our :code:`get_courses()` call:

.. code:: python

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

Keyword Arguments
~~~~~~~~~~~~~~~~~

Most of Canvas’s API endpoints accept a variety of arguments. CanvasAPI allows developers to insert keyword arguments when making calls to endpoints that accept arguments.

.. code:: python

    # Get all of the active courses a user is currently enrolled in
    >>> courses = user.get_courses(enrollment_status='active')

For a more detailed description of how CanvasAPI handles more complex keyword arguments, check out the `Keyword Argument Documentation <keyword-args.html>`_.

Smart DateTimes
~~~~~~~~~~~~~~~

CanvasAPI is set up to make working with datetime strings a little bit easier.

If Canvas's documentation calls for an ISO 8601 format datetime string, you can pass in a `Python datetime object <https://docs.python.org/3/library/datetime.html>`_ instead. For example, updating the :code:`start_at` and :code:`end_at` dates of a course:


.. code-block:: python

    from datetime import datetime

    start_date = datetime(2018, 1, 1, 0, 1)  # '2018-01-01T00:01Z'
    end_date = datetime(2018, 12, 31, 11, 59)  # '2018-12-31T11:59Z'

    course.update(
        course={
            'start_at': start_date,
            'end_at': end_date,
        }
    )

If Canvas returns an ISO 8601 formatted datetime string, CanvasAPI will automatically create a :code:`datetime` object from that string. This new :code:`datetime` object will be a the string attribute as the same key with :code:`_date` appended. For example, :code:`start_at` becomes :code:`start_at_date`. The attribute with the original string representation of the date is retained.

.. code-block:: python

    >>> course = canvas.get_course(1)
    >>> course.start_at
    '2014-02-11T16:38:00Z'
    >>> course.start_at_date
    datetime.datetime(2014, 2, 11, 16, 38, tzinfo=<UTC>)
