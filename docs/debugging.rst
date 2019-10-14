Debugging
==========

As you work with CanvasAPI, you may encounter responses that don't match your expectations. In some cases, fixing the discrepancy is as simple as realizing you've misspelled a parameter name. In others, the CanvasAPI library might be improperly handling your input, and you'll need to submit a pull request or a bug report to get it resolved. Sometimes Canvas itself may be responding erroneously.

Capturing Logs
-----------------
CanvasAPI emits logs for important events through the `standard logging module <https://docs.python.org/3/library/logging.html>`_. Inspecting these logs can make debugging much easier, as they provide a closer look at the abstracted network activity of the library. In order to view them, you'll need to tell Python where to put them.

A basic logging configuration might look like this:

.. code-block:: python

    import logging
    import sys

    logger = logging.getLogger("canvasapi")
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

Once configured, any log event in the ``canvasapi`` module namespace will be printed to ``sys.stdout``:

.. code:: python

    # A previously configured `Canvas` client
    >>> canvas.get_current_user()
    2019-07-08 14:22:24,517 - canvasapi.requester - INFO - Request: GET https://base/api/v1/users/self
    2019-07-08 14:22:24,517 - canvasapi.requester - DEBUG - Headers: {'Authorization': '****4BSt'}
    2019-07-08 14:22:24,748 - canvasapi.requester - INFO - Response: GET https://base/api/v1/users/self 200
    2019-07-08 14:22:24,749 - canvasapi.requester - DEBUG - Headers: {'Cache-Control': 'max-age=0, private, must-revalidate',
    'Connection': 'keep-alive',
    'Content-Encoding': 'gzip',
    'Content-Length': '329',
    'Content-Type': 'application/json; charset=utf-8',
    2019-07-08 14:22:24,749 - canvasapi.requester - DEBUG - Data: {'avatar_url': 'https://base/images/thumbnails/43244/Umo5dyAg0OS3tpDtDN',
    'created_at': '2014-08-22T08:02:00-04:00',
    'effective_locale': 'en',
    'email': '',
    'id': XXXX181,
    'integration_id': None,
    'locale': None,
    'login_id': 'XXXXXXXX181',
    'name': 'Some User',
    'permissions': {'can_update_avatar': True, 'can_update_name': False},
    'root_account': 'xxxxxx.edu',
    'short_name': 'Some User',
    'sis_user_id': 'XXXXXXXX181',
    'sortable_name': 'User S'}