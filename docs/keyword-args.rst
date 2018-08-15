Keyword Arguments
=================

Basic Parameters
----------------

In general, basic parameters can be passed directly as keyword arguments.

For example, :func:`canvasapi.course.Course.get_users` has several basic parameters including :code:`search_term` and :code:`user_id`, as shown in the `Canvas Docs for List Users in Course <https://canvas.instructure.com/doc/api/courses.html#method.courses.users>`_.

Given an existing :class:`canvasapi.course.Course` object, :code:`course`, the parameter :code:`search_term` can be passed like this:

.. code:: python

    course.get_users(search_term='John Doe')

Multiple basic arguments can be passed. In this case, :code:`enrollment_role` has also been added.

.. code:: python

    course.get_users(
        search_term='John Doe',
        enrollment_role='StudentEnrollment'
    )

List Parameters
---------------

Some endpoints have parameters that are designed to be passed a list. These usually look like :code:`foo[]`.

For example, :func:`canvasapi.course.Course.get_users` has a few list parameters: :code:`enrollment_type[]`, :code:`include[]`, :code:`user_ids[]`, and :code:`enrollment_state[]`, as shown in the `Canvas Docs for List Users in Course <https://canvas.instructure.com/doc/api/courses.html#method.courses.users>`_. To use these parameters, just pass a list to the keyword. CanvasAPI will automatically detect the list and convert the parameter to the right format. For instance, :code:`enrollment_type[]` can be passed like this:

.. code:: python

    course.get_users(enrollment_type=['teacher', 'student'])

Multiple list parameters can be passed, including in combination with basic parameters. For this example, :code:`include[]` and :code:`search_term` have been added. Note that even though only one option was sent to :code:`include[]`, it is still a list.

.. code:: python
    
    course.get_users(
        enrollment_type=['teacher', 'student'],
        search_term='John',
        include=['email']
    )

Nested Parameters
-----------------

Some endpoints have parameters that look like :code:`foo[bar]`. Typically, there will be multiple parameters with the same prefix in the same endpoint.

For example, :func:`canvasapi.account.Account.create_course` has several parameters that look like :code:`course[foo]`, as shown in the `Canvas Docs for Create a New Course <https://canvas.instructure.com/doc/api/courses.html#method.courses.create>`_. However, square brackets are not valid characters for Python variables, so the following would **NOT** work:

.. code:: python

    # This is not valid, and will not work.
    account.create_course(course[name]='Example Course')

What Canvas is effectively doing with the bracket format is grouping things into objects. To achieve a similar effect in Python, CanvasAPI uses dictionaries.

Given an existing :class:`canvasapi.account.Account` object, :code:`account`, the parameter :code:`course[name]` can be passed like this:

.. code:: python

    account.create_course(course={'name': 'Example Course'})

In the background, CanvasAPI will combine the keys of the dictionary with the keyword of the argument, and ultimately send the correct variable to Canvas.

The benefit of this pattern is that multiple parameters with the same prefix can be sent to the same keyword argument. So to pass the :code:`course[name]`, :code:`course[course_code]`, and :code:`course[is_public]` arguments, it would look like this:

.. code:: python

    account.create_course(
        course={
            'name': 'Example Course',
            'course_code': 'TST1234',
            'is_public': True
        }
    )

Nested parameters work easily alongside basic (and list) parameters. For example, :code:`offer` and :code:`enroll_me`:

.. code:: python

    account.create_course(
        course={
            'name': 'Example Course',
            'course_code': 'TST1234',
            'is_public': True
        },
        enroll_me=True,
        offer=False
    )

Complex Parameters
------------------

The three main types of parameters (basic, list, and nested) from above cover most types of parameters Canvas expects. However, there are some types that look deceptively more complex than they actually are. Below are some examples of how to handle these in CanvasAPI.

Deep Nested Parameters
~~~~~~~~~~~~~~~~~~~~~~

:func:`canvasapi.user.User.edit` has the parameter :code:`user[avatar][url]`, as shown in the `Canvas Docs for Edit a User <https://canvas.instructure.com/doc/api/users.html#method.users.update>`_. Any parameter that takes the form of :code:`foo[bar1][bar2]` with multiple bracketed sub-parameters follows the same rules as normal nested parameters, but with deeper nesting.

.. code:: python
    
    user.edit(
        user={
            'avatar': {
                'url': 'http://example.com/john_avatar.png'
            }
        }
    )

List of Nested Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~

:func:`canvasapi.account.Account.add_grading_standards` has the parameters :code:`grading_scheme_entry[][name]` and :code:`grading_scheme_entry[][value]`, as shown in the `Canvas Docs for Create a New Grading Standard <https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.create>`_. Any parameter that takes the form of :code:`foo[][bar]` can be represented by a list of dictionaries.

.. code:: python

    account.add_grading_standards(
        title='New Grading Standard',
        grading_scheme_entry=[
            {
                'name': 'A',
                'value': 90
            },
            {
                'name': 'B',
                'value': 80
            }
        ]
    )

Nested List Parameters
~~~~~~~~~~~~~~~~~~~~~~

:func:`canvasapi.course.Course.create_assignment` has the parameters :code:`assignment[submission_types][]` and :code:`assignment[allowed_extensions][]`, as shown in the `Canvas Docs for Create an Assignment <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.create>`_. Any parameter that takes the form of :code:`foo[bar][]` is a nested parameter of which the value is a list.

.. code:: python

    course.create_assignment(
        assignment={
            'name': 'Assignment 1',
            'submission_types': ['online_text_entry', 'online_upload'],
            'allowed_extensions': ['doc', 'docx']
        }
    )
