Exceptions
==========

CanvasAPI may return a number of different exceptions, which are listed below.

Quick Guide
------------

+-----------------------------------------------------+-----------------+---------------------------------------------------------------------------------+
| **Exception**                                       | **Status Code** | **Explanation**                                                                 |
+-----------------------------------------------------+-----------------+---------------------------------------------------------------------------------+
| :class:`~canvasapi.exceptions.BadRequest`           | 400             | Canvas was unable to process the request.                                       |
+-----------------------------------------------------+-----------------+---------------------------------------------------------------------------------+
| :class:`~canvasapi.exceptions.InvalidAccessToken`   | 401             | The supplied API key is invalid.                                                |
+-----------------------------------------------------+-----------------+---------------------------------------------------------------------------------+
| :class:`~canvasapi.exceptions.Unauthorized`         | 401             | CanvasAPI's key is valid, but is unauthorized to access the requested resource. |
+-----------------------------------------------------+-----------------+---------------------------------------------------------------------------------+
| :class:`~canvasapi.exceptions.Forbidden`            | 403             | Canvas has denied access to the resource for this user.                         |
+-----------------------------------------------------+-----------------+---------------------------------------------------------------------------------+
| :class:`~canvasapi.exceptions.ResourceDoesNotExist` | 404             | Canvas could not locate the requested resource.                                 |
+-----------------------------------------------------+-----------------+---------------------------------------------------------------------------------+
| :class:`~canvasapi.exceptions.Conflict`             | 409             | Canvas had a conflict with an existing resource.                                |
+-----------------------------------------------------+-----------------+---------------------------------------------------------------------------------+
| :class:`~canvasapi.exceptions.RequiredFieldMissing` | N/A             | A required keyword argument was not included.                                   |
+-----------------------------------------------------+-----------------+---------------------------------------------------------------------------------+
| :class:`~canvasapi.exceptions.CanvasException`      | N/A             | An unknown error was thrown.                                                    |
+-----------------------------------------------------+-----------------+---------------------------------------------------------------------------------+

Class Reference
----------------

.. autoclass:: canvasapi.exceptions.CanvasException
    :members:

    The :class:`~canvasapi.exceptions.CanvasException` exception is a basic library exception that all other exceptions inherit from. It is also thrown whenever an error occurs but a more specific exception isn't available or appropriate.

    Here's a simple example of catching a :class:`~canvasapi.exceptions.CanvasException`:

    .. code-block:: python

        from canvasapi.exceptions import CanvasException

        try:
            canvas.get_course(1)
        except CanvasException as e:
            print(e)

.. autoclass:: canvasapi.exceptions.BadRequest
    :members:

    The :class:`~canvasapi.exceptions.BadRequest` exception is thrown when Canvas returns an HTTP 400 error.

.. autoclass:: canvasapi.exceptions.InvalidAccessToken
    :members:

    The :class:`~canvasapi.exceptions.InvalidAccessToken` exception is thrown when Canvas returns an HTTP 401 error and includes a ``WWW-Authenticate`` header.

    This indicates that the supplied API Key is invalid.

.. autoclass:: canvasapi.exceptions.Unauthorized
    :members:

    The :class:`~canvasapi.exceptions.Unauthorized` exception is thrown when Canvas returns an HTTP 401 error and does **NOT** include a ``WWW-Authenticate`` header.

    This indicates that the supplied API Key is probably valid, but the calling user does not have permission to access this resource.

.. autoclass:: canvasapi.exceptions.ResourceDoesNotExist
    :members:

    The :class:`~canvasapi.exceptions.ResourceDoesNotExist` exception is thrown when Canvas returns an HTTP 404 error.

.. autoclass:: canvasapi.exceptions.RequiredFieldMissing
    :members:

    The :class:`~canvasapi.exceptions.RequiredFieldMissing` exception is thrown when required fields are not passed to a method's keyword arguments. This is common in cases where the required field must be represented as a dictionary. See our `documentation on keyword arguments <keyword-args.html>`_ for examples of how to use keyword arguments in CanvasAPI.

.. autoclass:: canvasapi.exceptions.Forbidden
    :members:

    The :class:`~canvasapi.exceptions.Forbidden` exception is thrown when Canvas returns an HTTP 403 error.

.. autoclass:: canvasapi.exceptions.Conflict
    :members:

    The :class:`~canvasapi.exceptions.Conflict` exception is thrown when Canvas returns an HTTP 409 error.
