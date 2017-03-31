Getting Started with canvasapi
===============================

Installing canvasapi
---------------------

You can install with pip::

    pip install canvasapi

Usage
-----

Before using canvasapi, you'll need to instantiate a new Canvas object:

.. code:: python
    
    from canvasapi import Canvas

    canvas = Canvas(API_KEY, API_URL)

You can now use :code:`canvas` to make API calls.

Most of the core endpoints are available. You can explore the `class reference <class-reference.html>`_ page
for indepth descriptions of each type's functionality (accounts, courses, etc.). 

Examples
--------

Let's write a script to print out all of the users in a course:

.. code:: python

    from canvasapi import Canvas, Course, User

    # Set up our Canvas object
    canvas = Canvas(API_KEY, API_URL)

    # First, retrieve the Course object
    course = canvas.get_course(1234567)

    # Grab the course's name
    print course.name

    # Grab the people in the course
    users = course.get_users()

    # Print out each user in the course
    for user in users:
        print user.name

We can update a course's information as well:

.. code:: python

    from canvasapi import Canvas, Course

     # Set up our Canvas object
    canvas = Canvas(API_KEY, API_URL)

    # First, retrieve the Course object
    course = canvas.get_course(1234567)

    # Construct a dictionary of new values for the course
    updated_course = {
        'name': 'Better Course 2',
        'course_code': 'BC002',
        'open_enrollment': True
    }

    # Update the course
    course.update(course=updated_course)
