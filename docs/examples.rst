Examples
========

Here are some examples of common tasks that can be performed easily and quickly with CanvasAPI.


Boilerplate
-----------

All other examples assume you have already created a :code:`canvas` object like so:

.. code-block:: python

    # Import the Canvas class
    from canvasapi import Canvas

    # Canvas API URL
    API_URL = "https://example.com"
    # Canvas API key
    API_KEY = "p@$$w0rd"

    # Initialize a new Canvas object
    canvas = Canvas(API_URL, API_KEY)


Accounts
--------

Creating a New User
~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    
    # Grab the account to create the user under
    account = canvas.get_account(1)

    user = account.create_user(
        user={
            'name': 'New User'            
        },
        pseudonym={
            'password': 'secure123',
            'sis_user_id': 'new_user'
        }
    )


List Courses under an Account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    
    courses = account.get_courses()

    for course in courses:
        print(course)


Users
-----


Get a User by SIS ID
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Grab a user with the SIS ID of 'some_id'
    user = canvas.get_user('some_id', 'sis_login_id')


Get a user by their Canvas ID
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    
    # Grab user with ID of 1
    user = canvas.get_user(1)


Edit an Existing User
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    
    # Grab the user
    user = canvas.get_user(1)

    user.edit(
        user={'name': 'New Name'}
    )


Get a User's Page Views
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    page_views = user.get_page_views()


Logins
------

List User Logins
~~~~~~~~~~~~~~~~

.. code-block:: python

    logins = user.get_user_logins()

    for login in logins:
        print(login)


Courses
-------


Get a Course by Canvas ID
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Grab course with ID of 123456
    course = canvas.get_course(123456)


Get Users in a Course
~~~~~~~~~~~~~~~~~~~~~~

Using :func:`canvasapi.course.Course.get_users`:

Get All Users
##############

.. code-block:: python

    users = course.get_users()

    for user in users:
        print(user)

Get Only Students
##################

.. code-block:: python

    users = course.get_users(enrollment_type=['student'])

    for user in users:
        print(user)

Get Only Teachers, TAs, and Designers
######################################

.. code-block:: python

    type_list = ['teacher', 'ta', 'designer']

    users = course.get_users(enrollment_type=type_list)

    for user in users:
        print(user)

Get Only Active and Invited Students And Teachers
##################################################

.. code-block:: python

    users = course.get_users(
        enrollment_type=['teacher', 'student']
        enrollment_state=['active', 'invited']
    )

    for user in users:
        print(user)


Update (Edit) a Course
~~~~~~~~~~~~~~~~~~~~~~

Using :func:`canvasapi.course.Course.update`:

Update Course Name
##################

.. code-block:: python

    print(course.name)  # prints 'Old Name'

    course.update(course={'name': 'New Name'})

    print(course.name)  # prints 'New Name'

Update Course Start and End Dates
#################################

Either an ISO8601 format date string:

.. code-block:: python

    course.update(
        course={
            'start_at': '2018-01-01T00:01Z',
            'end_at': '2018-12-31T11:59Z'
        }
    )

Or a Python `DateTime <https://docs.python.org/3/library/datetime.html>`_ object:

.. code-block:: python

    from datetime import datetime

    start_date = datetime(2018, 1, 1, 0, 1)
    end_date = datetime(2018, 12, 31, 11, 59)

    course.update(
        course={
            'start_at': start_date,
            'end_at': end_date
        }
    )


Conclude a Course
~~~~~~~~~~~~~~~~~

Using :func:`canvasapi.course.Course.conclude`:

.. code-block:: python

    course.conclude()


Delete a Course
~~~~~~~~~~~~~~~

Using :func:`canvasapi.course.Course.delete`:

.. code-block:: python

    course.delete()


Assignments
-----------


Get a Single Assignment
~~~~~~~~~~~~~~~~~~~~~~~

Using :func:`canvasapi.course.Course.get_assignment`:

.. code-block:: python

    # Grab assignment with ID of 1234
    assignment = course.get_assignment(1234)

    print(assignment)


Get Multiple Assignments
~~~~~~~~~~~~~~~~~~~~~~~~

Using :func:`canvasapi.course.Course.get_assignments`:

Get All Assignments
###################

.. code-block:: python

    assignments = course.get_assignments()

    for assignment in assignments:
        print(assignment)

Get Ungraded Assignments
########################

.. code-block:: python

    assignments = course.get_assignments(bucket='ungraded')

    for assignment in assignments:
        print(assignment)


Create an Assignment
~~~~~~~~~~~~~~~~~~~~

Using :func:`canvasapi.course.Course.create_assignment`:

Create a Basic Assignment
#########################

.. code-block:: python

    new_assignment = course.create_assignment({
        'name': 'Assignment 1'
    })

    print(new_assignment)

Create an Assignment with Multiple Submission Types
###################################################

.. code-block:: python

    new_assignment = course.create_assignment({
        'name': 'Assignment 2',
        'submission_types': ['online_upload', 'online_text_entry', 'online_url']
    })

    print(new_assignment)

Create a Complex Assignment
###########################

.. code-block:: python

    from datetime import datetime

    new_assignment = course.create_assignment({
        'name': 'Assignment 3',
        'submission_types': ['online_upload'],
        'allowed_extensions': ['docx', 'doc', 'pdf'],
        'notify_of_update': True,
        'points_possible': 100,
        'due_at': datetime(2018, 12, 31, 11, 59),
        'description': 'Please upload your homework as a Word document or PDF.',
        'published': True
    })

    print(new_assignment)


Update (Edit) an Assignment
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using :func:`canvasapi.assignment.Assignment.edit`:

Update an Assignment's Name
###########################

.. code-block:: python

    updated_assignment = assignment.edit(assignment={'name': 'New Name'})

    print(updated_assignment)

Change an Assignment's Submission Type(s)
#########################################

.. code-block:: python

    updated_assignment = assignment.edit(
        assignment={'submission_types': ['on_paper']}
    )

    print(updated_assignment)


Delete an Assignment
~~~~~~~~~~~~~~~~~~~~

Using :func:`canvasapi.assignment.Assignment.delete`:

.. code-block:: python

    assignment.delete()
