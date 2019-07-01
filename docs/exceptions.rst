Exceptions
==========

CanvasAPI may return a number of different exceptions, which are listed below.

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

    This indicates that while the supplied API Key is probably valid, the calling user does not have permission to access this resource.

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
